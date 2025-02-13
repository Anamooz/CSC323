"""
Name : Brian Kwong and Trycia Vong
"""

from pad import *
from tools import *
from constants import *
from Crypto.Cipher import AES


def ecb_encrypt(key: bytes, plaintext: bytes) -> bytes:
    padded_msg = pad(plaintext)
    ciphertext = b""
    aes_encrypter = AES.new(key, AES.MODE_ECB)
    for i in range(0, len(padded_msg), BLOCK_SIZE):
        block = padded_msg[i : i + BLOCK_SIZE]
        ciphertext += aes_encrypter(block)
    return ciphertext


def ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    plaintext = b""
    aes_decrypter = AES.new(key, AES.MODE_ECB)
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i : i + BLOCK_SIZE]
        plaintext += aes_decrypter.decrypt(block)
    return unpad(plaintext).decode()


try:
    with open("Lab2.TaskII.A.txt", "r") as f:
        ciphertext = base64.b64decode(f.read())
        key = b"CALIFORNIA LOVE!"
        print(ecb_decrypt(key, ciphertext))
except FileNotFoundError:
    exit("File not found")
