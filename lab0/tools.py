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


def getFrequency(string: str) -> dict:
    string = string.lower()
    freq = {}
    for i in string:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq


def countNumberOfCharacters(input_string: str) -> int:
    count = 0
    for s in input_string:
        if s.isalpha():
            count += 1
    return count


def indexCoincidence(inputText: str) -> float:
    freq = getFrequency(inputText)
    message_length = countNumberOfCharacters(inputText)
    numberOfChars = 26
    total = 0
    for i in range(numberOfChars):
        try:
            total += freq[chr(i + 97)] * (freq[chr(i + 97)] - 1)
        except KeyError:
            pass
    return total / ((message_length * (message_length - 1)) / numberOfChars)


print(indexCoincidence(input("Enter a string: ")))
