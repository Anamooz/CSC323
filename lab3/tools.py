"""
Name : Brian Kwong and Trycia Vong
"""

import base64
from constants import FREQUENCY
from typing import Dict, List


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
        return total / ((message_length * (message_length - 1)) / numberOfChars)
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
        input_string, False
    )  # Number of alphabet characters in the string
    difference_total = 0
    for key in freq:
        try:
            # Calculate the difference between the frequency of the letter in the text and the expected frequency
            # Frequency = (Number of occurences of the letter / Length of the string) * 100
            difference_total += abs(
                ((freq[key] / string_length) * 100) - FREQUENCY[key]
            )
        except (KeyError, ZeroDivisionError):
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

    return (
        abs(indexCoincidence(input_string) - 1.7) < 0.5
        and numberOfNonVowelWords(input_string) < 5
        and frequencyDifference(input_string) <= 1.5
        and validByteRange(input_string)
    )


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
        key
    ):  # Repeat the key if it is shorter than the input string
        number = len(inputString) // len(key) + 1
        key *= number
    return bytes(
        [a ^ b for a, b in zip(inputString, key)]
    )  # For every byte in the input string, XOR it with the corresponding byte in the key


def vowelCounter(char: str) -> int:
    """

    The following function checks if a character is a vowel

    Args:
    char (str): The string to be checked

    Returns:
    int: Number of vowels in the string

    """
    count = 0
    for s in char:
        if s.lower() in "aeiou":
            count += 1
    return count


def calculateVowelRatio(string: str) -> float:
    """

    The following function calculates the ratio of vowels to the total number of characters in a string

    Args:
    string (str): The string to be checked

    Returns:
    float: The ratio of vowels to the total number of characters in the string

    """

    try:
        ratio = vowelCounter(string) / countNumberOfCharacters(string, False)
        return ratio
    except ZeroDivisionError:
        return 0


def validByteRange(input: str) -> bool:
    """
    The following function checks if a given string contains only valid chartacters used in normal English text

    Args:
    input (str): The string to be checked

    Returns:
    bool: True if the string contains only valid characters, False otherwise

    """

    for i in input:
        if ord(i) > 126 or ord(i) < 32 and i not in ["\n", "\t", "\r"]:
            return False
    return True


def calculateSpaceRatio(string: str) -> float:
    """

    The following function calculates the ratio of spaces to the total number of characters in a string

    Args:
    string (str): The string to be checked

    Returns:
    float: The ratio of spaces to the total number of characters in the string

    """

    try:
        ratio = string.count(" ") / countNumberOfCharacters(string, True)
        return ratio
    except ZeroDivisionError:
        return 0


def findHighestToLowestCharacterFrequencyRatio(string: str) -> float:
    """
    The following function calculates the ratio of the highest character frequency to the lowest character frequency in a string

    Args:
    string (str): The string to be checked

    Returns:
    float: The ratio of the highest character frequency to the lowest character frequency in the string

    """

    if len(string) == 0:
        return 1

    freq = getFrequency(string)
    try:
        return max(freq.values()) / min(freq.values())
    except ZeroDivisionError:
        return max(freq.values())


def fileReaderHex(file: str) -> List[bytes]:
    """
    The following function reads in a file of hex encoded strings and converts
    them into ASCII bytes

    Args:
        file (str): The path to the file to be read

    Returns:
        List[bytes]: A list of bytes encoded as ASCII characters

    """

    with open(file, "r") as f:  # Opens the file in read mode
        lines: List[str] = f.readlines()  # Reads in all the lines of the file
        texts: List[str] = []
        for line in lines:  # Loops through each line in the file
            texts.append(
                bytes.fromhex(line.strip())
            )  # Converts the line from a hex string to bytes and appends it to the texts list
    return texts


def fileReaderBase64(file: str) -> List[bytes]:
    """
    The following function reads in a file in base64 encoding and
    returns a list of bytes encoded as ASCII characters
    The ASCII characters may or may not be printable

    Args:
    file (str): The path to the file to be read

    Returns:
    List[bytes]: A list of bytes encoded as ASCII characters
    """

    with open(
        file, "r"
    ) as f:  # Opens the file as f in read only mode ; BufferedReader f = new BufferedReader(new FileReader(file))
        text: List[str] = f.read().strip(
            "\n"
        )  # Removes all the new line characters from the text ; ArrayList<String> text = new ArrayList<>(Arrays.asList(f.read().split("\n")))
    return base64_to_ascii(
        text
    )  # Converts the base64 encoded text to ASCII characters in byte format ; Decoder decoder = Base64.getDecoder(); return decoder.decode(text)


def fileReaderASCII(file: str) -> List[bytes]:
    """
    The following function reads in a file and returns a list of bytes encoded as ASCII characters

    Args:
    file (str): The path to the file to be read

    Returns:
    List[bytes]: A list of bytes encoded as ASCII characters

    """

    with open(file, "r") as f:  # Opens the file in read mode
        lines: List[str] = f.readlines()  # Reads in all the lines of the file
        texts: List[bytes] = []
        for line in lines:  # Loops through each line in the file
            texts.append(
                line.strip().encode()
            )  # Converts the line from a string to bytes and appends it to the texts list
    return texts


def vigenèreSubtractor(cipher: bytes, key: bytes) -> bytes:
    """
    The following function takes in a string in ASCII text and subtracts the ASCII value of it from the ASCII value of the key
    It then returns the a new character with the result of the subtraction (shift)

    Args:
    cipher (bytes): The string to be decrypted
    key (bytes): The key to be used for decryption

    Returns:
    bytes: The decrypted string in ASCII text (bytes)

    """
    if type(key) is bytes:
        key = int.from_bytes(key, "little")

    letters = bytearray()

    for letter in cipher:
        letters.append(((letter - key) % 26) + 65)
    return bytes(letters)


def countNGramsRatio(text: str) -> int:
    text = text.lower()
    COMMON_NTH_GRAMS = [
        "th",
        "he",
        "in",
        "en",
        "nt",
        "re",
        "er",
        "an",
        "ti",
        "es",
        "on",
        "at",
        "se",
        "nd",
        "or",
        "ar",
        "al",
        "te",
        "co",
        "de",
        "to",
        "ra",
        "et",
        "ed",
        "it",
        "sa",
        "em",
        "ro",
        "the",
        "and",
        "tha",
        "ent",
        "ing",
        "ion",
        "tio",
        "for",
        "nde",
        "has",
        "nce",
        "edt",
        "tis",
        "oft",
        "sth",
        "men",
    ]
    count = 0
    for ngram in COMMON_NTH_GRAMS:
        count += text.count(ngram)
    return count / len(text)
