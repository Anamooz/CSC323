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
from multiprocessing import Process, Pool, Queue, cpu_count


DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
CORES = cpu_count()


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


def convertBytesToHex(data):
    return str(data.hex())


def hashGPU(transaction, previousBlockId, batch_size=2500000):
    size = 0
    attempts = 0
    gpu_block = cudf.Series([transaction + previousBlockId] * batch_size)
    while size == 0:
        nonces = cp.random.bytes(AES.block_size * len(gpu_block))
        # Convert the bytes to a numpy array
        np_nonce_bytes = np.frombuffer(nonces, dtype=np.uint8)
        # Convert bytes to hex
        nonces = np.array(
            [bytes(b).hex() for b in np_nonce_bytes.reshape(batch_size, AES.block_size)]
        )

        nonces = cudf.Series(nonces)
        combined_block = gpu_block + nonces
        hashed = combined_block.hash_values(method="sha256")

        # Convert the hash to a string\
        hashed = hashed.astype("str")
        # Filter hashes that are less than the difficulty
        hashed = hashed[hashed.str[:6] == "000000"]

        size = len(hashed)
        if size > 0:
            print(hashed)
            attempts += batch_size
            return hashed.iloc[0], attempts
        else:
            attempts += batch_size
        if attempts % batch_size == 0:
            print("Attempts: ", attempts)


def createBlock(transaction, previousBlockId, gpu=False):

    # Find the nonce as Proof of Work
    start = time.perf_counter()

    hashFunction = hashGPU if gpu else hashCPU
    nonce, attempts = hashFunction(transaction, previousBlockId)

    end = time.perf_counter()
    print("Time to find nonce: ", end - start)
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


from statistics import mean

# hasGPU = False
# try:
#     subprocess.check_output("nvidia-smi")
#     hasGPU = True
# except Exception:
#     pass
# print(createBlock(example_transaction, example_blockchain[0]["id"]))
previousBlockId = "12345"

megaHashes = {}

trails = [i * 100000 for i in range(40)]

for trials in trails:

    results = []
    for i in range(5):
        start = time.perf_counter()
        nonce, attempts = hashGPU(
            json.dumps(example_transaction, sort_keys=True), previousBlockId, 1000000
        )
        end = time.perf_counter()
        megaHash = attempts / (end - start) / 1000000
        results.append(megaHash)
    megaHashes[trials] = mean(results)
    print("MegaHashes per second: ", megaHashes[trials], "for", trials, "trials")

# Sort results by value
megaHashes = dict(sorted(megaHashes.items(), key=lambda item: item[1]))
print(megaHashes)
