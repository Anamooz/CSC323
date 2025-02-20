from string import ascii_letters
from random import choices
from Crypto.Hash import SHA1
from time import *

hashes = {}

i = 0
hash_function = SHA1.new()
while True:
    message = "".join(choices(ascii_letters, k=30))
    message_hashed = hash_function.update(message.encode())
    hash_function.hexdigest()

    # Get the first 50 bits of the hash
    message_hashed = bytes.fromhex(hash_function.hexdigest())[:6]

    if hashes.get(message_hashed.hex(), None) != None:
        print(
            f"Collision found: {message} and {hashes[message_hashed.hex()]} with hash {message_hashed.hex()} at iteration {i}"
        )
        break
    else:
        hashes[message_hashed.hex()] = message
    i += 1
    if i % 1000 == 0:
        print(f"{i} iterations completed")
