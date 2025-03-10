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
from ecdsa import VerifyingKey
from threading import Lock


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


def hashCPUHelper(data: bytes, queue: Queue, newBlock, reporter=False) -> None:
    """
    The following function mines ZackCoin using POW on the CPU
    It continues generates a new nonce hashes the data and nonce
    until the hash is less than the difficulty

    Each CPU core will run this function

    :param data: The data to be hashed (bytes)
    :param queue: The queue to store the nonce and attempts (Queue)
    :param newBlock: The event to check if a new block has been found (Event)
    :param reporter: A boolean to check if the function should print the number of attempts (bool)

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


def hashCPU(transaction: dict, previousBlockId: str) -> tuple[str, int]:
    """

    The following function manages the different mining process on the CPU
    Each core will have a seperate process to mine the block

    The first core to find the block will return the nonce and the number of attempts
    ALl other cores will be terminated

    If a new block is found, the process will be terminated and the nonce will be set to None through IPC events


    :param transaction: The transaction to be hashed (dict)
    :param previousBlockId: The previous block id (str)

    :return nonce: The nonce that satisfies the difficulty (str)
    :return attempts: The number of attempts to find the nonce (int)
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

    :param transaction: The transaction to be hashed (dict)
    :param previousBlockId: The previous block id (str)
    :param batch_size: The number of nonces to generate at a time (default is 1,000,000)

    """

    # Import the necessary libraries
    import cupy as cp
    import numpy as np
    import cudf

    # Initialize the variables
    size = 0  # Size of the number hashes that are less than the difficulty found
    attempts = 0  # Number of attempts to find the nonce
    # Allocate GPU memory for the block that stores the original block [transaction + previousBlockId] data.
    # Make batch_size copies of the block soopreations can be parallelized
    gpu_block = cudf.Series(
        [json.dumps(transaction, sort_keys=True) + previousBlockId] * batch_size
    )

    # Read in from global space to check if a new block has arrived
    global newBlockArrived

    # While the size of the hashes that are less than the difficulty is 0 and no new block has arrived
    while size == 0 and not newBlockArrived:

        # Generate batch size number of random nonces
        nonces = cp.random.bytes(AES.block_size * len(gpu_block))
        # Convert the bytes to a numpy array so we can convert each to a hex string
        # Each row is 16 bytes long
        # Batch size number of rows
        np_nonce_bytes = np.ndarray(
            (batch_size, AES.block_size), dtype=np.uint8, buffer=nonces
        )

        # For each row convert the bytes to a hex string
        nonces = np.array([bytes(b).hex() for b in np_nonce_bytes])

        # Copy that array to the GPU
        nonces = cudf.Series(nonces)

        # Vector add the two blocks together
        combined_block = gpu_block + nonces

        # For each row find their sha256 hash
        hashed = combined_block.hash_values(method="sha256")

        # Filter hashes that are less than the difficulty
        # Check if the first 6 characters are 0
        # 7th character is a number between 0 and 7
        hashed = hashed[hashed.astype("str").str.slice(0, 7) < "0000007"]

        # Get the size of the hashes that are less than the difficulty
        size = len(hashed)
        if size > 0:
            # Update the number of attempts
            attempts += batch_size

            # Check if there has been a new block if so this hash becomes invalid
            if newBlockArrived:
                break

            # Extract the nonce that generated the hash
            nonce = int(str(hashed).split(" ")[0])
            return nonces.iloc[nonce], attempts
        else:
            # Update the number of attempts
            attempts += batch_size
            print("Attempts: ", attempts)

    # If there is a nerw block discard the current nonce and re
    return None, attempts


def createBlock(
    transaction: dict, previousBlockId: str, publicKeys: VerifyingKey
) -> dict:
    """
    The following function creates a new block by adding the coinbase tranaction,
    Calculate/find the nonce that satisfies the difficulty and creates the proof of work
    The block is then returned with its nonce, prroof of work hash and coinbase tranaction inserted
    It also reports the speed of mining in MegaHashes per second
    Tranaction validality is checked before creating the block

    :param transaction: The valid transaction to be hashed and placed in the block (dict)
    :param previousBlockId: The previous block id (str)
    :param publicKeys: The public key of the miner (VerifyingKey)

    :return block: The new block with the coinbase transaction, nonce, proof of work hash and previous block id (dict)
    """

    # Adds the coinbase transaction to the transaction list
    transaction["output"].append(
        {
            "value": 50,
            "pub_key": publicKeys.to_string().hex(),
        }
    )

    # Start the timer to calculate the speed of mining
    start = time.perf_counter()

    # Determine the hash function to use
    hashFunction = hasGPU if hashGPU else hashCPU
    # Find the nonce as Proof of Work and calculate the proof of work hash
    nonce, attempts = hashFunction(transaction, previousBlockId)

    # Stop the performance timer
    end = time.perf_counter()

    # Clear the memory
    gc.collect()

    # Calculate the speed of mining and print it
    print("MegaHashes per second: ", attempts / (end - start) / 1000000)

    # If the nonce is None, return None means a new block came in
    if nonce is None:

        return None

    # Calculate the proof of work hash
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

    # Return the new block
    return block


def mine(client, lock: Lock, autoGenerate=False):
    """
    The following function picks a unverified transaction from the unverified transaction pool,
    verfies the transaction, calculates the correct nonce and proof of work hash and broadcasts the block to the network
    The function also writes the blockchain and unverified transaction pool to a file for logging purposes

    A valid transaction is:
        - Not already in the blockchain
        - Not a double spending transaction
        - Correctly signed by the sender (Verify using the public key)
        - Amounts are correct and in the correct format
            - Input == Output
            - Change is calculated appropriately
        - Input transactions are valid (in the blockchain)

    :param client: The client object that contains the blockchain and unverified transaction pool (Client)
    :param lock: A lock to indicate if the miner should continue mining (Lock)
    :param autoGenerate: A boolean to check if the miner should automatically generate transactions if the unverified transaction pool is empty (bool)

    :return: None
    """

    # Links in the  global vairable to see if a new block has arrived
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

    # Counter to keep track of the time since the last block was mined
    secondsSinceLastBlock = 0

    # While the lock is still engaged indicating the miner should continue mining
    while lock.locked():

        # Check if there are any unverified transactions in the UTX pool
        if len(client.utx) > 0:

            # Get the first transaction in the UTX pool
            transaction = client.utx.pop(0)

            # Check if the tx already in the blockchain
            try:
                if tx.inBlockchain(client.blockchain, transaction):
                    print("Transaction already in blockchain or double spending")
                    continue
                else:

                    # Get the last block in the blockchain
                    previousBlock = client.blockchain[-1]["id"]

                    # Verify the transaction
                    if tx.verify(client.blockchain, transaction):

                        # Creates a new block with a valid nonce and proof of work hash
                        # Updates tre transaction with coinbase transaction
                        new_block = createBlock(
                            transaction, previousBlock, client.pk, hasGPU
                        )

                        # Check if a new block was added by the network before miner can generate a block
                        if new_block is None:

                            # Wait until the newly added block is processed
                            while newBlockArrived:
                                time.sleep(1)

                            # Check if the block added by the network contains the same transaction
                            if tx.compareTransactions(
                                transaction, client.blockchain[-1]["tx"]
                            ):
                                # If so move onto the next transaction
                                print("Another miner found the block")
                            else:
                                # Try again with this transaction
                                client.utx.insert(0, transaction)

                            continue

                        # Send this new block to the network
                        client.send_to_nodes(new_block)

                        # Reset the counter of when the last block was mined
                        secondsSinceLastBlock = 0

                        # Clear the transaction
                        transaction = None

                        print("Block mined")

                        # Wait until the new block is processed
                        while newBlockArrived:
                            time.sleep(1)
                    else:
                        print("Transaction not valid")
            except Exception:
                print("Transaction not valid")
        else:

            # If the miner should automatically generate transactions after a certain idle time
            if autoGenerate and secondsSinceLastBlock > 30:
                # Generate a new transaction
                tx.newTransaction(client, client.sk, client.pk.to_string().hex(), 1)

                # Reset the counter of when the last block was mined
                secondsSinceLastBlock = 0

            # Sleep for 10 seconds and check for any new blocks
            time.sleep(10)

            # Increment the counter of when the last block was mined
            secondsSinceLastBlock += 10
