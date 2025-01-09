import base64


def ascii_to_hex(asciiText: str) -> str:
    return asciiText.encode().hex()


def hex_to_ascii(hex: str) -> str:
    return bytes.fromhex(hex).decode()


def ascii_to_base64(asciiText: str) -> str:
    return base64.b64encode(asciiText.encode()).decode()


# def ascii_to_base64(base64Bytes: bytes) -> str:
#     return base64.decode(base64Bytes)


print(ascii_to_base64("Hello, World!"))
