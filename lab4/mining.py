import hashlib
import json
from Crypto import Random
from Crypto.Cipher import AES
from exampleTransaction import example_transaction, example_blockchain
import time
import subprocess
import cupy as cp
import numpy as np
import cudf
from multiprocessing import Process, Queue, cpu_count
import transaction as tx


DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
CORES = cpu_count()

hasGPU = False
try:
    subprocess.check_output("nvidia-smi")
    hasGPU = True
except Exception:
    pass


def hashCPUHelper(data, queue, reporter=False):
    nonce = Random.new().read(AES.block_size).hex()
    attempts = 0
    while (
        int(
            hashlib.sha256(data + nonce.encode("utf-8")).hexdigest(),
            16,
        )
        > DIFFICULTY
    ):
        nonce = Random.new().read(AES.block_size).hex()
        attempts += 1
        if reporter and attempts % 1000000 == 0:
            print("Attempts: ", attempts * CORES)
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


def hashGPU(transaction, previousBlockId, batch_size=3200000):
    size = 0
    attempts = 0
    gpu_block = cudf.Series(
        [json.dumps(transaction, sort_keys=True) + previousBlockId] * batch_size
    )
    while size == 0:
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
        hashed = hashed[hashed.astype("str").str.startswith("000000")]

        size = len(hashed)
        if size > 0:
            nonce = int(str(hashed).split(" ")[0])
            attempts += batch_size
            return nonces.iloc[nonce], attempts
        else:
            attempts += batch_size

        if attempts % batch_size == 0:
            print("Attempts: ", attempts)


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

    end = time.perf_counter()
    print("MegaHashes per second: ", attempts / (end - start) / 1000000)

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


def mine(client, lock):
    while lock.locked():
        if len(client.utx) > 0:
            transaction = client.utx.pop(0)
            previousBlock = client.blockchain[-1]["id"]
            if tx.verify(client.blockchain, transaction):

                new_block = createBlock(transaction, previousBlock, client.pk, hasGPU)
                # Check if any new blocks were added to the blockchain
                # Have to redo
                while new_block["prev"] != client.blockchain[-1]["id"]:
                    previousBlock = client.blockchain[-1]["id"]
                    new_block = createBlock(
                        transaction, previousBlock, client.pk, hasGPU
                    )
                if tx.verifyBlock(client.blockchain, new_block):
                    client.blockchain.append(new_block)
                    client.blockChainSize += 1
                    client.send_to_nodes(new_block)
                    client.wallet, client.balance = tx.calculateUserBalance(
                        client.blockchain, client.sk
                    )
                    print("Block mined")
                else:
                    print("Block not valid")
            else:
                print("Transaction not valid")
        time.sleep(1)
