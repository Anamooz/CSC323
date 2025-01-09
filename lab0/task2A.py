def implementXOR(inputString: bytes, key: bytes) -> bytes:
    return bytes([a ^ b for a, b in zip(inputString, key)])