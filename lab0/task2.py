from tools import *
from typing import List


def fileReader(file: str) -> List[bytes]:
    with open(file, "r") as f:  # Opens the file in read mode
        lines = f.readlines()  # Reads in all the lines of the file
        texts = []
        for line in lines:  # Loops through each line in the file
            texts.append(
                bytes.fromhex(line.strip())
            )  # Converts the line from a hex string to bytes and appends it to the texts list
    return texts


def singleXORHelperLooper(texts: List[bytes]) -> None:
    for key in range(256):
        singleXORHelper(texts, int.to_bytes(key, 1))


def singleXORHelper(texts: List[bytes], key: bytes) -> List[bytes]:
    extracted_text: List[bytes] = []
    for text in texts:
        extracted_text.append(implementXOR(text, key))  # 0x610x650xF6 --> "Ae.."
    english_text = []
    for text in extracted_text:
        if isEnglish(text.decode(errors="ignore")):
            english_text.append(text.decode(errors="ignore"))
    if len(english_text) > 0:
        print("Key: ", int(hex(key[0]), 16))
        print("Possible ", english_text)


singleXORHelperLooper(fileReader("Lab0.TaskII.B.txt"))
