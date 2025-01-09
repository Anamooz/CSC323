import base64


# Converts an ASCII string to hex encoding
def ascii_to_hex(asciiText: bytes) -> str:
    return asciiText.hex()


# Converts an hex encoded string to ASCII text
def hex_to_ascii(hexString: str) -> bytes:
    return bytes.fromhex(hexString)


# Converts an ASCII string to base64 encoding
def ascii_to_base64(asciiText: bytes) -> str:
    return base64.b64encode(asciiText).decode()


# Converts base64 encoded string to ASCII text
def base64_to_ascii(base64Bytes: str) -> bytes:
    return base64.b64decode(base64Bytes.encode())


x = ascii_to_hex("Hello:".encode())
print(x)
print(hex_to_ascii(x))
