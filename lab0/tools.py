import base64
from constants import FREQUENCY
from typing import Dict


def ascii_to_hex(asciiText: bytes) -> str:
    """
    Converts an ASCII string to hex encoding

    Args:
    asciiText (bytes): ASCII text (in bytes) to be converted to hex encoding

    Returns:
    str: String containing the hex encoding of the ASCII text

    """

    return asciiText.hex()


def hex_to_ascii(hexString: str) -> bytes:
    """
    Converts an hex encoded string to ASCII text

    Args:
    hexString (str): Hex encoded string to be converted to ASCII text

    Returns:
    bytes: ASCII text (in bytes) of the hex encoded string

    """

    return bytes.fromhex(hexString)


def ascii_to_base64(asciiText: bytes) -> str:
    """
    Converts an ASCII bytes to base64 encoding in string format

    Args:
    asciiText (bytes): ASCII text (in bytes) to be converted to base64 encoding

    Returns:
    str: String containing the base64 encoding of the ASCII text

    """

    return base64.b64encode(asciiText).decode()


# Converts base64 encoded string to ASCII text
def base64_to_ascii(base64Bytes: str) -> bytes:
    """

    Converts a base64 encoded string to ASCII text

    Args:
    base64Bytes (str): base64 encoded string to be converted to ASCII text

    Returns:
    bytes: ASCII text (in bytes) of the base64 encoded string

    """

    return base64.b64decode(base64Bytes.encode())


def hasVowel(input_string: str) -> bool:
    """
    Function to check if a string has at least one vowel after decrypting attempt

    Args:
    input_string (str): The string to be checked

    Returns:
    bool: True if the string has at least one vowel, False otherwise

    """

    vowels = "aeiou"
    count = 0
    for s in input_string.lower():
        if s in vowels:
            count += 1
    return count >= 1


def getFrequency(string: str) -> Dict[str, int]:
    """

    The following function finds the numbers of occurences of each character in a string after decrypting attempt

    Args:
    string (str): The string to be checked

    Returns:
    Dict[str, int]: A dictionary containing the number of occurences of each character in the string

    """

    string = string.lower()
    freq = {}
    for i in string:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq


def countNumberOfCharacters(input_string: str, spaces: bool) -> int:
    """
    The following funcion finds the number of alphabet characters in a string after decrypting attempt
    Alaphabet characters are defined as "A-Z" and "a-z"
    Counting spaces is optional

    Args:
    input_string (str): The string to be checked
    spaces (bool): If True, spaces will be counted as alphabet characters

    Returns:
    int: The number of alphabet characters in the string

    """

    count = 0
    for s in input_string:
        if s.isalpha() or (spaces and s == " "):
            count += 1
    return count


#
def indexCoincidence(inputText: str) -> float:
    """
    The following function counts the index of coincidence of a string for English after decrypting attempt

    Args:
    inputText (str): The string to be checked

    Returns:
    float: The index of coincidence of the string

    """

    freq = getFrequency(inputText)
    message_length = countNumberOfCharacters(inputText, False)
    numberOfChars = 26
    total = 0
    for i in range(numberOfChars):
        try:
            total += freq[chr(i + 97)] * (freq[chr(i + 97)] - 1)
        except KeyError:  # Letter does not exist in the text
            pass
    try:
        return total / ((message_length *
                         (message_length - 1)) / numberOfChars)
    except ZeroDivisionError:
        return 0


def numberOfNonVowelWords(input_string: str) -> int:
    """

    The following function finds the number of words in a string that do not contain any vowels after decrypting attempt

    Args:
    input_string (str): The string to be checked

    Returns:
    int: The number of words in the string that do not contain any vowels

    """

    words = input_string.split()
    return len(list(filter(lambda x: not hasVowel(x), words)))


def frequencyDifference(input_string: str) -> float:
    """

    The following function calculates the frequency difference in percentage
    of the decrypted text from the expected frequency of English text

    Args:
    input_string (str): The string to be checked

    Returns:
    float: The frequency difference in percentage

    """

    freq = getFrequency(input_string)
    string_length = countNumberOfCharacters(
        input_string)  # Number of alphabet characters in the string
    difference_total = 0
    for key in freq:
        try:
            # Calculate the difference between the frequency of the letter in the text and the expected frequency
            # Frequency = (Number of occurences of the letter / Length of the string) * 100
            difference_total += abs(((freq[key] / string_length) * 100) -
                                    FREQUENCY[key])
        except KeyError:
            try:
                # Letter doesnt exist in our decrypted text
                # Give frequency % of 0
                difference_total += abs(0 - FREQUENCY[key])
            except KeyError:
                pass  # Non alphabet character Ignored
    return difference_total / len(FREQUENCY)


def isEnglish(input_string: str) -> bool:
    """

    The following function checks if a given string is English or not given the following factors:
    1. Index of Coincidence is close to 1.7
    2. Number of words without vowels is less than 2
    3. Frequency difference distribution is less than 1.5

    Args:
    input_string (str): The string to be checked

    Returns:
    bool: True if the string is English, False otherwise

    """

    return (abs(indexCoincidence(input_string) - 1.7) < 0.3
            and numberOfNonVowelWords(input_string) < 2
            and frequencyDifference(input_string) <= 1.5)


def implementXOR(inputString: bytes, key: bytes) -> bytes:
    """

    The following function implements the XOR operation on two byte strings

    Args:
    inputString (bytes): The input string (in bytes) to be XORed
    key (bytes): The key (in bytes) to be XORed with the input string

    Returns:
    bytes: The XORed string

    """

    if len(inputString) > len(
            key):  # Repeat the key if it is shorter than the input string
        number = len(inputString) // len(key) + 1
        key *= number
    return bytes(
        [a ^ b for a, b in zip(inputString, key)]
    )  # For every byte in the input string, XOR it with the corresponding byte in the key
