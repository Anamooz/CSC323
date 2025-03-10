import hashlib
import json
from Crypto import Random
from Crypto.Cipher import AES
import time
import subprocess
from multiprocessing import Process, Queue, cpu_count
import transaction as tx
import os
import gc


newBlockArrived = False
DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
CORES = cpu_count()

hasGPU = False
try:
    subprocess.check_output("nvidia-smi")
    hasGPU = False
except Exception:
    pass


def hashCPUHelper(data, queue, reporter=False):
    global newBlockArrived

    nonce = Random.new().read(AES.block_size).hex()
    attempts = 0
    while (
        int(
            hashlib.sha256(data + nonce.encode("utf-8")).hexdigest(),
            16,
        )
        > DIFFICULTY
        and not newBlockArrived
    ):
        nonce = Random.new().read(AES.block_size).hex()
        attempts += 1
        if reporter and attempts % 1000000 == 0:
            print("Attempts: ", attempts * CORES)
    if newBlockArrived:
        nonce = None
    queue.put((nonce, attempts))


def hashCPU(transaction, previousBlockId):
    data = json.dumps(transaction, sort_keys=True).encode(
        "utf8"
    ) + previousBlockId.encode("utf-8")
    process_list = []
    queue = Queue()
    for i in range(CORES - 1):
        p = Process(target=hashCPUHelper, args=(data, queue, i == 0))
        process_list.append(p)
        p.start()
    for process in process_list:
        process.join()
        break
    for process in process_list:
        process.terminate()
    result = queue.get()
    return result[0], result[1] * (CORES - 1)


def hashGPU(transaction, previousBlockId, batch_size=1000000):

    import cupy as cp
    import numpy as np
    import cudf

    size = 0
    attempts = 0
    gpu_block = cudf.Series(
        [json.dumps(transaction, sort_keys=True) + previousBlockId] * batch_size
    )
    global newBlockArrived
    while size == 0 and not newBlockArrived:
        print("New block arrived: ", newBlockArrived)
        nonces = cp.random.bytes(AES.block_size * len(gpu_block))
        # Convert the bytes to a numpy array
        np_nonce_bytes = np.ndarray(
            (batch_size, AES.block_size), dtype=np.uint8, buffer=nonces
        )
        # Convert bytes to hex
        nonces = np.array([bytes(b).hex() for b in np_nonce_bytes])

        nonces = cudf.Series(nonces)
        combined_block = gpu_block + nonces
        hashed = combined_block.hash_values(method="sha256")

        # Filter hashes that are less than the difficulty
        # Check if the first 6 characters are 0
        # 7th character is a number between 0 and 7

        hashed = hashed[hashed.astype("str").str.slice(0, 7) < "0000007"]

        size = len(hashed)
        if size > 0:
            nonce = int(str(hashed).split(" ")[0])
            attempts += batch_size
            if newBlockArrived:
                break
            return nonces.iloc[nonce], attempts
        else:
            attempts += batch_size

        if attempts % batch_size == 0:
            print("Attempts: ", attempts)
    return None, attempts


def createBlock(transaction, previousBlockId, publicKeys, gpu=False):

    # Adds the coinbase transaction to the transaction list
    transaction["output"].append(
        {
            "value": 50,
            "pub_key": publicKeys.to_string().hex(),
        }
    )

    # Find the nonce as Proof of Work
    start = time.perf_counter()

    hashFunction = hashGPU if hashGPU else hashCPU
    nonce, attempts = hashFunction(transaction, previousBlockId)

    gc.collect()

    end = time.perf_counter()
    print("MegaHashes per second: ", attempts / (end - start) / 1000000)

    if nonce is None:

        return None

    proof_of_work = hashlib.sha256(
        json.dumps(transaction, sort_keys=True).encode("utf8")
        + previousBlockId.encode("utf-8")
        + nonce.encode("utf-8")
    ).hexdigest()

    # Create a new block
    block = {
        "type": 0,
        "id": hashlib.sha256(
            json.dumps(transaction, sort_keys=True).encode("utf8")
        ).hexdigest(),
        "prev": previousBlockId,
        "tx": transaction,
        "nonce": nonce,
        "pow": proof_of_work,
    }

    return block


def mine(client, lock, autoGenerate=False):

    # Sets this thread with the highest priority
    # This is to ensure that the mining thread is always running
    # even if the other threads are running

    # Check platform

    global newBlockArrived

    try:
        # Windows
        if os.name == "nt":
            import win32api
            import win32process
            import win32con

            handle = win32api.GetCurrentThread()
            win32process.SetThreadPriority(handle, win32process.THREAD_PRIORITY_HIGHEST)
            print("Thread priority set to highest")
        # Unix/Linux
        elif os.name == "posix" or hasattr(os, "sched_get_priority_max"):
            policy = os.sched_getscheduler(0)
            param = os.sched_param(os.sched_get_priority_max(policy))
            os.sched_setscheduler(0, policy, param)
            print("Thread priority set to highest")
        else:
            # Unsupported OS
            pass
    except Exception:
        # If the sys admin disabled the priority change
        # Or some other error
        # Just run mine with normal priority
        print("Couldn't set thread priority")
        pass

    # Write block to file
    with open("blockchain.json", "w") as f:
        jsonstr = json.dumps(client.blockchain, indent=4)
        f.write(jsonstr)

    # Write utx to file
    with open("utx.json", "w") as f:
        jsonstr = json.dumps(client.utx, indent=4)
        f.write(jsonstr)

    secondsSinceLastBlock = 0

    while lock.locked():
        if len(client.utx) > 0:

            transaction = client.utx.pop(0)

            # Check if the tx already in the blockchain

            if tx.inBlockchain(client.blockchain, transaction):
                print("Transaction already in blockchain or double spending")
                continue
            else:
                previousBlock = client.blockchain[-1]["id"]
                if tx.verify(client.blockchain, transaction):

                    new_block = createBlock(
                        transaction, previousBlock, client.pk, hasGPU
                    )

                    if new_block is None:

                        # Wait until the new block is processed

                        while newBlockArrived:
                            time.sleep(1)

                        if tx.compareTransactions(
                            transaction, client.blockchain[-1]["tx"]
                        ):
                            print("Another miner found the block")
                        else:
                            # Try again with this block
                            client.utx.insert(0, transaction)

                        continue

                    # Write block to file
                    with open("blockchain.json", "w") as f:
                        jsonstr = json.dumps(client.blockchain, indent=4)
                        f.write(jsonstr)

                    client.send_to_nodes(new_block)
                    secondsSinceLastBlock = 0
                    transaction = None
                    print("Block mined")

                    while newBlockArrived:
                        time.sleep(1)
                else:
                    print("Transaction not valid")
        else:
            if autoGenerate and secondsSinceLastBlock > 30:
                tx.newTransaction(client, client.sk, client.pk.to_string().hex(), 1)
                secondsSinceLastBlock = 0
            time.sleep(10)
            secondsSinceLastBlock += 10
