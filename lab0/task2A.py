def implementXOR(inputString: bytes, key: bytes) -> bytes:
    if len(inputString) > len(key):
        number = (len(inputString) // len(key) + 1)
        key *= number
    return bytes([a ^ b for a, b in zip(inputString, key)])

print(implementXOR("ABCDEF".encode(), "AB".encode()))