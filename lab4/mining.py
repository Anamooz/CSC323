import hashlib
import json
from Crypto import Random
from Crypto.Cipher import AES
import time
import subprocess
from multiprocessing import Process, Queue, cpu_count, Event
import transaction as tx
import os
import platform
import gc


newBlockArrived = False
DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
CORES = cpu_count()


def detectGPUSupport():
    """
    This function checks if mining can be done on the GPU
    It checks if the GPU is available and if the necessary libraries are installed
    As of right now only NVIDIA GPUs (10x series or higher) are supported

    :return: None

    """

    subprocess.check_output("nvidia-smi")

    # Check if Linux
    if platform.system() == "Linux":
        subprocess.check_output("nvcc --version")
    else:
        print(
            "Only Linux is supported for GPU mining Using Windows? install WSL to continue with GPU mining"
        )
        input("Press enter to continue with CPU mining")
        raise Exception()

    import cupy as cp
    import numpy as np
    import cudf

    # Test if the GPU is available
    np.zeros(1)
    cp.zeros(1)
    cudf.Series([1, 2, 3])
    return


# Set false by default
hasGPU = False
try:
    # Check if the GPU is available and if the necessary libraries are installed
    detectGPUSupport()
    hasGPU = True
except ModuleNotFoundError:
    print("Did you make sure to install the GPU dependencies?")
    input("Press enter to continue with CPU mining")
except Exception:
    pass


def hashCPUHelper(data, queue, newBlock, reporter=False):
    """
    The following function mines ZackCoin using POW on the CPU
    It continues generates a new nonce hashes the data and nonce
    until the hash is less than the difficulty

    Each CPU core will run this function

    :param data: The data to be hashed
    :param queue: The queue to store the nonce and attempts
    :param newBlock: The event to check if a new block has been found
    :param reporter: A boolean to check if the function should print the number of attempts

    :return: None
    """

    # Initialize the nonce and number of attempts
    nonce = Random.new().read(AES.block_size).hex()
    attempts = 0

    # Hash the data and nonce together using sha256 and check if the digest is less than the difficulty
    # If the digest is greater than the difficulty, generate a new nonce and hash again
    while (
        int(
            hashlib.sha256(data + nonce.encode("utf-8")).hexdigest(),
            16,
        )
        > DIFFICULTY
        and not newBlock.is_set()
    ):

        # Generate a new nonce
        nonce = Random.new().read(AES.block_size).hex()

        # Increment the number of attempts
        attempts += 1

        # Print the number of attempts if the reporter is set to True
        if reporter and attempts % 1000000 == 0:
            print("Attempts: ", attempts * CORES)

    # If a new block has been found, set the nonce to None
    if newBlock.is_set():
        nonce = None

    # Put the nonce and number of attempts in the queue
    queue.put((nonce, attempts))


def hashCPU(transaction, previousBlockId) -> tuple[str, int]:
    """

    The following function manages the different mining process on the CPU
    Each core will have a seperate process to mine the block

    The first core to find the block will return the nonce and the number of attempts
    ALl other cores will be terminated

    If a new block is found, the process will be terminated and the nonce will be set to None through IPC events


    :param transaction: The transaction to be hashed
    :param previousBlockId: The previous block id

    :return nonce: The nonce that satisfies the difficulty
    :return attempts: The number of attempts to find the nonce
    """

    # Converts the tranaction and previous block id to seralized json bytes to be hashed
    data = json.dumps(transaction, sort_keys=True).encode(
        "utf8"
    ) + previousBlockId.encode("utf-8")

    # Initialize the process list queue and event
    process_list = []
    queue = Queue()
    newBlockEvent = Event()

    # For each core of the CPU other than the main core, create a new process
    for i in range(CORES - 1):
        # The first core will be the reporter
        # Create and start each process
        p = Process(target=hashCPUHelper, args=(data, queue, newBlockEvent, i == 0))
        # Append the process to the process list
        process_list.append(p)
        p.start()
    # While no process has found the block, wait for the queue to be empty
    while queue.empty():
        # Sleep for a second and check if a new block has been found or if the process has been terminated
        time.sleep(1)
        # If a new block has been found, set the event and wait for the process to terminate
        if newBlockArrived and not newBlockEvent.is_set():
            newBlockEvent.set()

    # Terminate all remaining processes
    for process in process_list:
        process.terminate()
        process.join()

    # Get the result from the queue
    result = queue.get()

    # Return the nonce and the number of attempts
    return result[0], result[1] * (CORES - 1)


def hashGPU(
    transaction: dict, previousBlockId: str, batch_size: int = 1000000
) -> tuple[str, int]:
    """
    This function performs mining using NVIDIA CUDA platform leverging GPU acceleration
    It uses cupy forGPU accleration of generating nonces
    It uses the NVIDIA CuDF library to perform the hashing and filtering of the hashes
    NOTE: This function is only supported on Linux and requires the installation of the necessary libraries
            - AMD and Intel GPUs are not supported
            - Windows users must install WSL and the Nivida CUDA toolkit to use this function
            - Minimum GPU requirement is the NVIDIA GPU with CUDA 11.2 and Compute Capability 6.0 or higher (GTX 16x series or higher)
                - CUDA 11.x must be installed

    :param transaction: The transaction to be hashed
    :param previousBlockId: The previous block id
    :param batch_size: The number of nonces to generate at a time (default is 1,000,000)

    """

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


def createBlock(transaction, previousBlockId, publicKeys):

    # Adds the coinbase transaction to the transaction list
    transaction["output"].append(
        {
            "value": 50,
            "pub_key": publicKeys.to_string().hex(),
        }
    )

    # Find the nonce as Proof of Work
    start = time.perf_counter()

    hashFunction = hasGPU if hashGPU else hashCPU
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

    global newBlockArrived

    # Sets this thread with the highest priority
    # This is to ensure that the mining thread is always running
    # even if the other threads are running
    # Check platform and apply the appropriate command to set the thread priority

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
            try:
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
            except Exception:
                print("Transaction not valid")
        else:
            if autoGenerate and secondsSinceLastBlock > 30:
                tx.newTransaction(client, client.sk, client.pk.to_string().hex(), 1)
                secondsSinceLastBlock = 0
            time.sleep(10)
            secondsSinceLastBlock += 10
