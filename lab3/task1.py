import requests
from tools import *

EAVESDROP_URL = "http://localhost:8080/eavesdrop"
SUBMIT_URL = "http://localhost:8080/submit"
ORCALE_URL = "http://localhost:8080?enc="


def paddingOracleAttackSingleBlock(iv, previous_block, cipherTextBlock):
    BLOCK_SIZE = 16
    modfied_new_block = bytearray(16)
    plainText = bytearray(16)

    # For each block, we need to decrypt each byte
    for i in range(BLOCK_SIZE):
        if i == 0:
            for j in range(0, 256):
                modfied_new_block[15 - i] = previous_block[15 - i] ^ j ^ 1
                newCipherText = iv + modfied_new_block + cipherTextBlock
                response = requestSession.get(ORCALE_URL + ascii_to_hex(newCipherText))
                if response.status_code == 404:
                    plainText[15] = j
                    break
        else:
            for j in range(0, i):
                modfied_new_block[15 - j] = (
                    previous_block[15 - j] ^ plainText[15 - j] ^ (i + 1)
                )
            for j in range(0, 256):
                modfied_new_block[15 - i] = previous_block[15 - i] ^ j ^ (i + 1)
                newCipherText = iv + modfied_new_block + cipherTextBlock
                response = requestSession.get(ORCALE_URL + ascii_to_hex(newCipherText))
                if response.status_code == 404:
                    plainText[15 - i] = j
                    break
    print("Block decrypted")
    return plainText


requestSession = requests.Session()
response = requestSession.get(EAVESDROP_URL)
cipherText = response.text.split('<p><font color="red">')[1].split("</font></p>")[0]
cipherText = hex_to_ascii(cipherText)
cipherText = bytearray(cipherText)
iv = cipherText[:16]
for i in range(0, len(cipherText) // 16 - 1):
    previous_block = cipherText[16 * i : (16 * (i + 1))]
    cipherText_block = cipherText[16 * (i + 1) : 16 * (i + 2)]
    plain_text = paddingOracleAttackSingleBlock(iv, previous_block, cipherText_block)
    plain_text += bytes(plain_text)
print(plain_text.decode())
