"""
Name : Brian Kwong and Trycia Vong
"""

from pad import *
from tools import *
from constants import *
from Crypto.Cipher import AES


def cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pad(plaintext)
    blocks = [plaintext[i : i + 16] for i in range(0, len(plaintext), 16)]
    ciphertext = iv
    for block in blocks:
        block = implementXOR(block, iv)
        iv = cipher.encrypt(block)
        ciphertext += iv
    return ciphertext


def cbc_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    blocks = [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]
    plaintext = b""
    for block in blocks:
        decrypted = cipher.decrypt(block)
        plaintext += implementXOR(decrypted, iv)
        iv = block
    plaintext = unpad(plaintext)
    return plaintext


KEY = "MIND ON MY MONEY"
IV = "MONEY ON MY MIND"
with open("Lab2.TaskIII.A.txt", "r") as f:
    cipertext = f.read()
    cipertext = base64_to_ascii(cipertext)
    ciphertext = IV.encode() + cipertext
    plaintext = cbc_decrypt(cipertext, KEY.encode())
    print(plaintext.decode())
