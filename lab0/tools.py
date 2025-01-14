import base64
from constants import FREQUENCY


# Converts an ASCII string to hex encoding
def ascii_to_hex(asciiText: bytes) -> str:
    return asciiText.hex()


# Converts an hex encoded string to ASCII text
def hex_to_ascii(hexString: str) -> bytes:
    return bytes.fromhex(hexString)


# Converts an ASCII string to base64 encoding in string format
def ascii_to_base64(asciiText: bytes) -> str:
    return base64.b64encode(asciiText).decode()


# Converts base64 encoded string to ASCII text
def base64_to_ascii(base64Bytes: str) -> bytes:
    return base64.b64decode(base64Bytes.encode())


# Testing our encode and decode functions
# x = ascii_to_hex("Hello:".encode())
# print(x)
# print(hex_to_ascii(x))


# Function to check if a string has at least one vowel after decrypting attempt
def hasVowel(input_string: str) -> bool:
    vowels = "aeiou"
    count = 0
    for s in input_string.lower():
        if s in vowels:
            count += 1
    return count >= 1


# The following function finds the numbers of occurences of each character in a string after decrypting attempt
def getFrequency(string: str) -> dict:
    string = string.lower()
    freq = {}
    for i in string:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq


# The following funcion finds the number of alphabet characters in a string after decrypting attempt
# Alaphabet characters are defined as "A-Z" and "a-z"
def countNumberOfCharacters(input_string: str) -> int:
    count = 0
    for s in input_string:
        if s.isalpha():
            count += 1
    return count


# The following function counts the index of coincidence of a string for English after decrypting attempt
def indexCoincidence(inputText: str) -> float:
    freq = getFrequency(inputText)
    message_length = countNumberOfCharacters(inputText)
    numberOfChars = 26
    total = 0
    for i in range(numberOfChars):
        try:
            total += freq[chr(i + 97)] * (freq[chr(i + 97)] - 1)
        except KeyError:  # Letter does not exist in the text
            pass
    try:
        return total / ((message_length * (message_length - 1)) / numberOfChars)
    except ZeroDivisionError:
        return 0


# The following function finds the number of words in a string that do not contain any vowels after decrypting attempt
def numberOfNonVowelWords(input_string: str) -> int:
    words = input_string.split()
    return len(list(filter(lambda x: not hasVowel(x), words)))


def frequencyDifference(input_string: str) -> float:
    freq = getFrequency(input_string)
    string_length = countNumberOfCharacters(
        input_string
    )  # Number of alphabet characters in the string
    difference_total = 0
    for key in freq:
        try:
            # Calculate the difference between the frequency of the letter in the text and the expected frequency
            # Frequency = (Number of occurences of the letter / Length of the string) * 100
            difference_total += abs(
                ((freq[key] / string_length) * 100) - FREQUENCY[key]
            )
        except KeyError:
            try:
                # Letter doesnt exist in our decrypted text
                # Give frequency % of 0
                difference_total += abs(0 - FREQUENCY[key])
            except KeyError:
                pass  # Non alphabet character Ignored
    return difference_total / len(FREQUENCY)


def isEnglish(input_string: str) -> bool:
    return (
        abs(indexCoincidence(input_string) - 1.7) < 0.3
        and numberOfNonVowelWords(input_string) < 2
        and frequencyDifference(input_string) <= 1.5
    )


def implementXOR(inputString: bytes, key: bytes) -> bytes:
    if len(inputString) > len(
        key
    ):  # Repeat the key if it is shorter than the input string
        number = len(inputString) // len(key) + 1
        key *= number
    return bytes(
        [a ^ b for a, b in zip(inputString, key)]
    )  # For every byte in the input string, XOR it with the corresponding byte in the key
