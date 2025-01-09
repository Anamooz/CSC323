import base64


# Converts an ASCII string to hex encoding
def ascii_to_hex(asciiText: str) -> str:
    return asciiText.encode().hex()


# Converts an hex encoded string to ASCII text
def hex_to_ascii(hex: str) -> str:
    return bytes.fromhex(hex).decode()


# Converts an ASCII string to base64 encoding
def ascii_to_base64(asciiText: str) -> str:
    return base64.b64encode(asciiText.encode()).decode()


# Converts base64 encoded string to ASCII text
def base64_to_ascii(base64Bytes: str) -> str:
    return base64.b64decode(base64Bytes.encode()).decode()


x = ascii_to_hex("Hello:")
print(x)
print(hex_to_ascii(x))
