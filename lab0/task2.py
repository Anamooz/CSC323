from tools import *
from typing import List, Tuple, Callable
from multiprocessing import Queue, Process
from itertools import product


class KeyAttributes:
    def __init__(
        self,
        key: int,
        index_of_coincidence: float,
        vowel_ratio: float,
        space_ratio: float,
    ):
        self.key = key
        self.index_of_coincidence = index_of_coincidence
        self.vowel_ratio = vowel_ratio
        self.space_ratio = space_ratio

    def __str__(self):
        return f"Key: {self.key} | Index of Coincidence: {self.index_of_coincidence} | Vowel Ratio: {self.vowel_ratio} | Space Ratio: {self.space_ratio} | Valid Key: {self.valid_key()}"

    def __repr__(self):
        return self.__str__()

    def valid_key(self) -> bool:
        return (
            self.vowel_ratio > 0.25
            and self.vowel_ratio < 0.5
            and abs(self.index_of_coincidence - 1.7) < 0.25
            and self.space_ratio > 0.1
            and self.space_ratio < 0.25
        )


# --- Filters for detemining what keys/text to keep ---
SINGLE_BYTE_XOR_KEY_FILTER = lambda text: isEnglish(text)
MUTI_BYTE_XOR_KEY_FILTER = lambda text: abs((indexCoincidence(text) - 1.7)) < 0.3
MUTI_BYTE_XOR_SUB_STRING_INITAL_FILTER = lambda text: chr(text[0]).isalpha()
MUTI_BYTE_XOR_SUB_STRING_FILTER = lambda single_byte_key_possibilities: (
    list(
        filter(
            lambda text: (validByteRange(text[1][0])),
            single_byte_key_possibilities,
        )
    )
)

# --- Reading File IO Functions ---


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


# --- Single Byte XOR Functions ---
def singleXORCracker(
    texts: List[bytes], predicate: Callable[[str], int]
) -> List[Tuple[int, str]]:
    """

    The following function performs a single byte XOR on a list of text and a key
    The function loops over all 256 different possible keys and returns the keys and the texts
    it believes to be in English
    The predicate is used to detemine whether the text is in English or not

    Args:
    texts (List[bytes]): A list of different strings represented in bytes that need to be decrypted using a single byte XOR
    predicate (Callable[[str], int]): A function that takes in a string and returns an booleean indcating whether the text resembles English or not This function should be deteministic and return a binary "Yes" or "No" reponse

    Returns:
    List[Tuple[int, str]]: A list of tuples where the first element is a potential key and the second element is the text that particular key would decrypt the text to to

    """

    # Creates an array to store all possible keys and texts combinations
    possible_keys_texts: List[Tuple[int, str]] = []

    # For all possible keys for a single byte XOR
    # for(int key = 0; key < 256; key++)
    for key in range(256):
        # k : is the key used to decrypt the text
        # string : is the decrypted text
        k, string = singleByteXORDecoder(texts, int.to_bytes(key, 1), predicate)
        if string is not None:  # If there is a match
            possible_keys_texts.append(
                (k, string)
            )  # Add the key and the text to the list of possible keys text combinations
    return possible_keys_texts  # Return the list of possible keys text combinations


def singleByteXORDecoder(
    texts: List[bytes], key: bytes, predicate: Callable[[str], bool]
) -> List[bytes]:
    """

    The following function performs a single byte XOR on a list of text and a key
    It will attempt to decrypt the text by XORing it with the key
    Afterwards the list of decrypted texts will be classfied by the predicate function
    It will return the key and either the assioscated text if the text passes the predicate function or (key, None) otherwise
    The predicate function is used to determine whether the text is in English or not


    Args:
    texts (List[bytes]): A list of different strings represented in bytes that need to be decrypted using a single byte XOR
    predicate (Callable[[str], int]): A function that takes in a string and returns an booleean indcating whether the text resembles English or not This function should be deteministic and return a binary "Yes" or "No" reponse

    Returns:
    Tuple[int, str]: A tuple where the first element is the key and the second element is the text of a match is foound or key, None oyherwise

    """

    # Creates a list to store all the decrypted texts
    extracted_text: List[bytes] = []

    # Creates a list to store all the texts that are in English
    english_text: List[str] = []

    # For all the texts in the list
    for text in texts:

        # Attempt to decrypt the text by XORing it with the key
        extracted_text.append(implementXOR(text, key))  # Ex : 0x610x650xF6 --> "Ae.."

    # For all the texts that have been decrypted
    for text in extracted_text:

        # Classify the text by the predicate function
        # If it passes it is classfied as English
        if predicate(text.decode(errors="ignore")):
            english_text.append(text.decode(errors="ignore"))

    # For all text that is classified as English given this key
    if len(english_text) > 0:
        # Return the key and the decrypted text
        return (int(hex(key[0]), 16), english_text)
    else:
        # Otherwise return the key and None
        return (int(hex(key[0]), 16), None)


# --- Muti-Byte XOR Functions ---


def mutiByteKeyBySingleByteXOR(texts: List[bytes], position: int, q: Queue):
    """

    The following function is a wrapper around single byte XOR that allows the process to be
    parallelized.  It takes in the poistion which is the subset of the text its responsible
    and a queue to place the results in once all key combinations for that byte have been exhausted

    Args:
    texts (List[bytes]): A list of strings represented in bytes that need to be decrypted using a single byte XOR
    position (int): The nth positions of the text that this process is responsible for where n is a integer between 1 and the key size
    queue (Queue): A muti-process queue to store the results of the process

    Returns:
    None: The function does not return anything but instead places the results in the queue.  This (child) process will exit after the execution of this function

    """

    # Calculates the possible keys for a single byte XOR of this position and text
    possible_keys = singleXORCracker(texts, MUTI_BYTE_XOR_KEY_FILTER)

    # Returns the possible keys and text combinations to the queue for parent process to collect and process
    return q.put([position, possible_keys])


# -- Muti-byte deteming key size ---


def keySizeIndexOfCoincidenceCalculator(text: bytes) -> bool:
    """
    The following function attempts to calculate the index of coincidence for a given text and key size
    Given a single byte key the function will attempt to loop through all possible combinations of that byte and find the `average`
    index of coincidence of all 256 different combinations
    A lower difference index of coincidence value indicates that the text is more likely to be English

    Args:
    text (bytes): The text that is encrypted

    Returns:
    bool : If this key size has the potential to be the correct key size

    """

    # For each possible key in a single byte XOR of a given length
    # For every possible key in a single byte XOR; for(int key = 0; key < 256; key++)
    # for(int key = 0; key < 256; key++)
    for key in range(256):

        # For every key in this single byte XOR try that key and use it to decrypt the text
        # If the decrypyed text contains only valid characters then it has a high chance of being the correct key size
        english = implementXOR(text, int.to_bytes(key, 1)).decode(errors="ignore")
        if validByteRange(english):
            return (
                True,
                indexCoincidence(english),
                calculateVowelRatio(english),
                calculateSpaceRatio(english),
            )

    # If all keys have been exhausted and none of them have produced a valid text then the key size is incorrect
    return (False, 0, 0, 0)


def mutiByteXORKeyProcess(text: bytes, keySize: int, queue: Queue) -> None:
    """

    The following function collects the nth subset of a given string where n is the key-size being tested
    and calculate the `average`index of coincidence for that subset of the text

    Example:
    If the 2nd position is choosen given the string "Paimon is not emergency food" the following characters will be taken into the string : "amsnreeeod"

    Args:
    text (bytes): The text that is encrypted
    keySize (int): The key size that is being tested between 1 and 20
    queue (Queue): A muti-process queue to store the results of the process and return the average index of coincidence value for that key size to the parent process

    Returns:
    None: The function does not return anything but instead places the results in the queue.  This (child) process will exit after the execution of this function
    """

    # Collects a subsrting of the text that is a composed of every nth character where n is the key size
    # This is completed using list comprehension
    sub_text = [text[i] for i in range(len(text)) if i % keySize == 0]

    # Grabs the nth character in a ASCII string if n is a mutiple of the keySize
    key_info = keySizeIndexOfCoincidenceCalculator(sub_text)
    key: KeyAttributes = None
    if key_info[0]:
        key = KeyAttributes(keySize, key_info[1], key_info[2], key_info[3])
    queue.put((keySize, key))


def mutiByteXORKeySearch(text: bytes) -> int:
    """

    The following function finds the ideal key size
    for the muti-byte XOR by minimuzing the index of coincidence difference from ideal English (1.7)
    This function utilizes mutiiple processes each reponsible for a particular key size
    This function will then return the key size with the smallest `avergae` index of coincidence value compared to ideal English

    Args:
    text (bytes): The text that is encrypted

    Returns:
    int: The `ideal` key size with the smallest `average` index of coincidence value compared to perfect English

    """

    # Creates a queue for muutiprocessing; Queue q = new Queue()
    q: Queue = Queue()
    # Creates a list to store all processes; List<Process> process_list = new ArrayList<>()
    process_list: List[Process] = []
    # Creates a list to store all index of coincidence values and their respective key sizes; List<List<int, int>> indexCoincidenceValues = new ArrayList<>()
    indexCoincidenceValues: List[List[int, int]] = []

    # For all key sizes between 1 and 20 ; for(int i = 1; i < 20; i++)
    for i in range(1, 20):
        # Create a process for each key size ; Process process = new Process(mutiByteXORHelper, text, i, q)
        process = Process(target=mutiByteXORKeyProcess, args=(text, i, q))
        # Append the key size to the process list ; process_list.add(process)
        process_list.append(process)
        # Starts the process ; process.start()
        process.start()

    # Wait for all processes to complete
    for p in process_list:
        # For each process wait for it to complete Then call p.join() to collect the child back from the OS; p.join()
        p.join()

    # Retrieve results from all child processes
    # While the queue is not empty ; while(!q.empty())
    while not q.empty():
        # Collect the result and append it to the indexCoincidenceValues list ; indexCoincidenceValues.add(q.get())
        indexCoincidenceValues.append(q.get())

    indexCoincidenceValues = filter(lambda x: x[1] is not None, indexCoincidenceValues)

    # Prints a formatted table of the index of coincidence values for all key sizes between 1 and 20
    print(
        f"Index of Coincidence Values for keys between 1 & 20 \n{'-'*20}\n"
        + "Key Size | Index of Coincidence\n"
        + "\n".join([f"{key}" for key in indexCoincidenceValues])
        + "\n"
        + "-" * 20
    )

    # # Return the key size with the smallest index of coincidence value
    # return indexCoincidenceValues[0][0]


# --- Muti-Byte XOR Decryption Functions ---


def constructStrings(possible_keys) -> List[Tuple[List[int], str]]:
    """

    The following function reconstructs all possible keys and text combinations given a list of keys and their assiosated substrings
    The output will be a list of all possible combinations in the following format <List[int], str> where the first element is a list of keys and the second element is the combined decrypted text

    Args:
    possible_keys (List[List[int, str]]): A list of keys and their assiosated substrings

    Returns:
    List[int, str]: A list of all possible combinations of keys and text

    """

    strings_keys_list: List[Tuple[List[int], str]] = []

    # Construct all different combinations of keys using the cartesian product
    number_of_combinations = [
        range(len(possible_keys[i])) for i in range(len(possible_keys))
    ]
    for item in list(product(*number_of_combinations)):
        # Iniiates two arrays for storing the two keys and decrypted text
        keys = []
        decrypted_text = []

        # For each of the keys
        for i in range(len(item)):
            # Get the key value
            keys.append(possible_keys[i][item[i]][0])
            # Get the substring of the text that is assioscated with that key
            decrypted_text.append(possible_keys[i][item[i]][1])

        # The following loop reconstructs the text from appending each character from each substring one character at a time
        j = 0
        string = ""

        # While there are still chcaracters in the text to append
        while len(decrypted_text) > 0:
            # Collect that character and append it to the string
            string += decrypted_text[j % len(decrypted_text)][0]
            # If there are no more characters in the substring remove it from the list
            if len(decrypted_text[j % len(decrypted_text)]) > 1:
                decrypted_text[j % len(decrypted_text)] = decrypted_text[
                    j % len(decrypted_text)
                ][1:]
            else:
                # Otherwise pop that character off from the substring
                decrypted_text.pop(j % len(decrypted_text))
            j += 1
        strings_keys_list.append((keys, string))
    return strings_keys_list


def decryptMutliByteXOR(text: bytes, keySize: int) -> None:
    """
    The following function decrypts a mutibyte XOR encrypted text given a key size of N bytes
    To decrypt each process will be responsible for brute forcing a single byte XOR on a subset of text
    Results will be filtered using the `MUTI_BYTE_XOR_KEY_FILTER` which checks the index of coincidence value of a given subset of text
    Currently the margin of error is 0.25 but can changed in the predicate
    The function will use mutiple processes each responsible for decrypting part of the text
    The results will then be joined together to form the final decrypted text or texts

    Args:
    text (bytes): The text that is in need of decryption

    Returns:
    List[Tuple[List[int], str]]: A list of tuples where the first element is a list of key composing the muti-byte key and the second element is the decrypted text

    Example:
    Collect the results from each queue
    Match the each part of the text with the correct key
    Make a list of all different combvinations
    For instance given a key size of 5 and 3 results form each process decrypted_parts could look like
    decrypted_parts[0] = [[15, "aZcde"], [26, "Cadeb"], [123, "Liaeg"]]
    decrppted_parts[1] = [[76, "a   o"], [99, "Gw2 a"], [123, "  dPh"]]
    decrypted_parts[2] = [[5, "zicd"], [39, " eFdl!"], [180, "kzea "]]
    decrypted_parts[3] = [[29, "tU  D"], [155, "usuo!"], [218, "Lsect"]]
    decrypted_parts[4] = [[51, "qweAT"], [77,"d ! d"], [188, "l tg!"]]
    which would provide the following combinations
    Keys  [15, 76, 5, 29, 51] aaztqZ iUwc c ed d AeoDT
    Keys  [15, 76, 5, 29, 77] aaztdZ iU c c !d d  eoDd
    Keys  [15, 76, 5, 29, 188] aaztlZ iU c c td d geoD!
    Keys  [15, 76, 5, 155, 51] aazuqZ iswc cued doAeo!T
    Keys  [15, 76, 5, 155, 77] aazudZ is c cu!d do eo!d
    Keys  [15, 76, 5, 155, 188] aazulZ is c cutd dogeo!!
    Keys  [15, 76, 5, 218, 51] aazLqZ iswc ceed dcAeotT
    Keys  [15, 76, 5, 218, 77] aazLdZ is c ce!d dc eotd
    Keys  [15, 76, 5, 218, 188] aazLlZ is c cetd dcgeot!
    Keys  [15, 76, 39, 29, 51] aa tqZ eUwc F ed d AelDTo!
    Keys  [15, 76, 39, 29, 77] aa tdZ eU c F !d d  elDdo!
    Keys  [15, 76, 39, 29, 188] aa tlZ eU c F td d gelD!o!
    Keys  [15, 76, 39, 155, 51] aa uqZ eswc Fued doAel!To!
    Keys  [15, 76, 39, 155, 77] aa udZ es c Fu!d do el!do!
    Keys  [15, 76, 39, 155, 188] aa ulZ es c Futd dogel!!o!
    Keys  [15, 76, 39, 218, 51] aa LqZ eswc Feed dcAeltTo!
    Keys  [15, 76, 39, 218, 77] aa LdZ es c Fe!d dc eltdo!
    Keys  [15, 76, 39, 218, 188] aa LlZ es c Fetd dcgelt!o!
    Keys  [15, 76, 180, 29, 51] aaktqZ zUwc e ed a Ae DTo
    Keys  [15, 76, 180, 29, 77] aaktdZ zU c e !d a  e Ddo
    Keys  [15, 76, 180, 29, 188] aaktlZ zU c e td a ge D!o
    Keys  [15, 76, 180, 155, 51] aakuqZ zswc eued aoAe !To
    Keys  [15, 76, 180, 155, 77] aakudZ zs c eu!d ao e !do
    Keys  [15, 76, 180, 155, 188] aakulZ zs c eutd aoge !!o
    Keys  [15, 76, 180, 218, 51] aakLqZ zswc eeed acAe tTo
    Keys  [15, 76, 180, 218, 77] aakLdZ zs c ee!d ac e tdo
    Keys  [15, 76, 180, 218, 188] aakLlZ zs c eetd acge t!o
    Keys  [15, 99, 5, 29, 51] aGztqZwiUwc2c ed d AeaDT
    Keys  [15, 99, 5, 29, 77] aGztdZwiU c2c !d d  eaDd
    Keys  [15, 99, 5, 29, 188] aGztlZwiU c2c td d geaD!
    Keys  [15, 99, 5, 155, 51] aGzuqZwiswc2cued doAea!T
    Keys  [15, 99, 5, 155, 77] aGzudZwis c2cu!d do ea!d
    Keys  [15, 99, 5, 155, 188] aGzulZwis c2cutd dogea!!
    Keys  [15, 99, 5, 218, 51] aGzLqZwiswc2ceed dcAeatT
    Keys  [15, 99, 5, 218, 77] aGzLdZwis c2ce!d dc eatd
    Keys  [15, 99, 5, 218, 188] aGzLlZwis c2cetd dcgeat!
    Keys  [15, 99, 39, 29, 51] aG tqZweUwc2F ed d AelDTa!
    Keys  [15, 99, 39, 29, 77] aG tdZweU c2F !d d  elDda!
    Keys  [15, 99, 39, 29, 188] aG tlZweU c2F td d gelD!a!
    Keys  [15, 99, 39, 155, 51] aG uqZweswc2Fued doAel!Ta!
    Keys  [15, 99, 39, 155, 77] aG udZwes c2Fu!d do el!da!
    Keys  [15, 99, 39, 155, 188] aG ulZwes c2Futd dogel!!a!
    Keys  [15, 99, 39, 218, 51] aG LqZweswc2Feed dcAeltTa!
    Keys  [15, 99, 39, 218, 77] aG LdZwes c2Fe!d dc eltda!
    Keys  [15, 99, 39, 218, 188] aG LlZwes c2Fetd dcgelt!a!
    Keys  [15, 99, 180, 29, 51] aGktqZwzUwc2e ed a Ae DTa
    Keys  [15, 99, 180, 29, 77] aGktdZwzU c2e !d a  e Dda
    Keys  [15, 99, 180, 29, 188] aGktlZwzU c2e td a ge D!a
    Keys  [15, 99, 180, 155, 51] aGkuqZwzswc2eued aoAe !Ta
    Keys  [15, 99, 180, 155, 77] aGkudZwzs c2eu!d ao e !da
    Keys  [15, 99, 180, 155, 188] aGkulZwzs c2eutd aoge !!a
    Keys  [15, 99, 180, 218, 51] aGkLqZwzswc2eeed acAe tTa
    Keys  [15, 99, 180, 218, 77] aGkLdZwzs c2ee!d ac e tda
    Keys  [15, 99, 180, 218, 188] aGkLlZwzs c2eetd acge t!a
    Keys  [15, 123, 5, 29, 51] a ztqZ iUwcdc edPd AehDT
    Keys  [15, 123, 5, 29, 77] a ztdZ iU cdc !dPd  ehDd
    Keys  [15, 123, 5, 29, 188] a ztlZ iU cdc tdPd gehD!
    Keys  [15, 123, 5, 155, 51] a zuqZ iswcdcuedPdoAeh!T
    Keys  [15, 123, 5, 155, 77] a zudZ is cdcu!dPdo eh!d
    Keys  [15, 123, 5, 155, 188] a zulZ is cdcutdPdogeh!!
    Keys  [15, 123, 5, 218, 51] a zLqZ iswcdceedPdcAehtT
    Keys  [15, 123, 5, 218, 77] a zLdZ is cdce!dPdc ehtd
    Keys  [15, 123, 5, 218, 188] a zLlZ is cdcetdPdcgeht!
    Keys  [15, 123, 39, 29, 51] a  tqZ eUwcdF edPd AelDTh!
    Keys  [15, 123, 39, 29, 77] a  tdZ eU cdF !dPd  elDdh!
    Keys  [15, 123, 39, 29, 188] a  tlZ eU cdF tdPd gelD!h!
    Keys  [15, 123, 39, 155, 51] a  uqZ eswcdFuedPdoAel!Th!
    Keys  [15, 123, 39, 155, 77] a  udZ es cdFu!dPdo el!dh!
    Keys  [15, 123, 39, 155, 188] a  ulZ es cdFutdPdogel!!h!
    Keys  [15, 123, 39, 218, 51] a  LqZ eswcdFeedPdcAeltTh!
    Keys  [15, 123, 39, 218, 77] a  LdZ es cdFe!dPdc eltdh!
    Keys  [15, 123, 39, 218, 188] a  LlZ es cdFetdPdcgelt!h!
    Keys  [15, 123, 180, 29, 51] a ktqZ zUwcde edPa Ae DTh
    Keys  [15, 123, 180, 29, 77] a ktdZ zU cde !dPa  e Ddh
    Keys  [15, 123, 180, 29, 188] a ktlZ zU cde tdPa ge D!h
    Keys  [15, 123, 180, 155, 51] a kuqZ zswcdeuedPaoAe !Th
    Keys  [15, 123, 180, 155, 77] a kudZ zs cdeu!dPao e !dh
    Keys  [15, 123, 180, 155, 188] a kulZ zs cdeutdPaoge !!h
    Keys  [15, 123, 180, 218, 51] a kLqZ zswcdeeedPacAe tTh
    Keys  [15, 123, 180, 218, 77] a kLdZ zs cdee!dPac e tdh
    Keys  [15, 123, 180, 218, 188] a kLlZ zs cdeetdPacge t!h
    Keys  [26, 76, 5, 29, 51] Caztqa iUwd c ee d AboDT
    Keys  [26, 76, 5, 29, 77] Caztda iU d c !e d  boDd
    Keys  [26, 76, 5, 29, 188] Caztla iU d c te d gboD!
    Keys  [26, 76, 5, 155, 51] Cazuqa iswd cuee doAbo!T
    Keys  [26, 76, 5, 155, 77] Cazuda is d cu!e do bo!d
    Keys  [26, 76, 5, 155, 188] Cazula is d cute dogbo!!
    Keys  [26, 76, 5, 218, 51] CazLqa iswd ceee dcAbotT
    Keys  [26, 76, 5, 218, 77] CazLda is d ce!e dc botd
    Keys  [26, 76, 5, 218, 188] CazLla is d cete dcgbot!
    Keys  [26, 76, 39, 29, 51] Ca tqa eUwd F ee d AblDTo!
    Keys  [26, 76, 39, 29, 77] Ca tda eU d F !e d  blDdo!
    Keys  [26, 76, 39, 29, 188] Ca tla eU d F te d gblD!o!
    Keys  [26, 76, 39, 155, 51] Ca uqa eswd Fuee doAbl!To!
    Keys  [26, 76, 39, 155, 77] Ca uda es d Fu!e do bl!do!
    Keys  [26, 76, 39, 155, 188] Ca ula es d Fute dogbl!!o!
    Keys  [26, 76, 39, 218, 51] Ca Lqa eswd Feee dcAbltTo!
    Keys  [26, 76, 39, 218, 77] Ca Lda es d Fe!e dc bltdo!
    Keys  [26, 76, 39, 218, 188] Ca Lla es d Fete dcgblt!o!
    Keys  [26, 76, 180, 29, 51] Caktqa zUwd e ee a Ab DTo
    Keys  [26, 76, 180, 29, 77] Caktda zU d e !e a  b Ddo
    Keys  [26, 76, 180, 29, 188] Caktla zU d e te a gb D!o
    Keys  [26, 76, 180, 155, 51] Cakuqa zswd euee aoAb !To
    Keys  [26, 76, 180, 155, 77] Cakuda zs d eu!e ao b !do
    Keys  [26, 76, 180, 155, 188] Cakula zs d eute aogb !!o
    Keys  [26, 76, 180, 218, 51] CakLqa zswd eeee acAb tTo
    Keys  [26, 76, 180, 218, 77] CakLda zs d ee!e ac b tdo
    Keys  [26, 76, 180, 218, 188] CakLla zs d eete acgb t!o
    Keys  [26, 99, 5, 29, 51] CGztqawiUwd2c ee d AbaDT
    Keys  [26, 99, 5, 29, 77] CGztdawiU d2c !e d  baDd
    Keys  [26, 99, 5, 29, 188] CGztlawiU d2c te d gbaD!
    Keys  [26, 99, 5, 155, 51] CGzuqawiswd2cuee doAba!T
    Keys  [26, 99, 5, 155, 77] CGzudawis d2cu!e do ba!d
    Keys  [26, 99, 5, 155, 188] CGzulawis d2cute dogba!!
    Keys  [26, 99, 5, 218, 51] CGzLqawiswd2ceee dcAbatT
    Keys  [26, 99, 5, 218, 77] CGzLdawis d2ce!e dc batd
    Keys  [26, 99, 5, 218, 188] CGzLlawis d2cete dcgbat!
    Keys  [26, 99, 39, 29, 51] CG tqaweUwd2F ee d AblDTa!
    Keys  [26, 99, 39, 29, 77] CG tdaweU d2F !e d  blDda!
    Keys  [26, 99, 39, 29, 188] CG tlaweU d2F te d gblD!a!
    Keys  [26, 99, 39, 155, 51] CG uqaweswd2Fuee doAbl!Ta!
    Keys  [26, 99, 39, 155, 77] CG udawes d2Fu!e do bl!da!
    Keys  [26, 99, 39, 155, 188] CG ulawes d2Fute dogbl!!a!
    Keys  [26, 99, 39, 218, 51] CG Lqaweswd2Feee dcAbltTa!
    Keys  [26, 99, 39, 218, 77] CG Ldawes d2Fe!e dc bltda!
    Keys  [26, 99, 39, 218, 188] CG Llawes d2Fete dcgblt!a!
    Keys  [26, 99, 180, 29, 51] CGktqawzUwd2e ee a Ab DTa
    Keys  [26, 99, 180, 29, 77] CGktdawzU d2e !e a  b Dda
    Keys  [26, 99, 180, 29, 188] CGktlawzU d2e te a gb D!a
    Keys  [26, 99, 180, 155, 51] CGkuqawzswd2euee aoAb !Ta
    Keys  [26, 99, 180, 155, 77] CGkudawzs d2eu!e ao b !da
    Keys  [26, 99, 180, 155, 188] CGkulawzs d2eute aogb !!a
    Keys  [26, 99, 180, 218, 51] CGkLqawzswd2eeee acAb tTa
    Keys  [26, 99, 180, 218, 77] CGkLdawzs d2ee!e ac b tda
    Keys  [26, 99, 180, 218, 188] CGkLlawzs d2eete acgb t!a
    Keys  [26, 123, 5, 29, 51] C ztqa iUwddc eePd AbhDT
    Keys  [26, 123, 5, 29, 77] C ztda iU ddc !ePd  bhDd
    Keys  [26, 123, 5, 29, 188] C ztla iU ddc tePd gbhD!
    Keys  [26, 123, 5, 155, 51] C zuqa iswddcueePdoAbh!T
    Keys  [26, 123, 5, 155, 77] C zuda is ddcu!ePdo bh!d
    Keys  [26, 123, 5, 155, 188] C zula is ddcutePdogbh!!
    Keys  [26, 123, 5, 218, 51] C zLqa iswddceeePdcAbhtT
    Keys  [26, 123, 5, 218, 77] C zLda is ddce!ePdc bhtd
    Keys  [26, 123, 5, 218, 188] C zLla is ddcetePdcgbht!
    Keys  [26, 123, 39, 29, 51] C  tqa eUwddF eePd AblDTh!
    Keys  [26, 123, 39, 29, 77] C  tda eU ddF !ePd  blDdh!
    Keys  [26, 123, 39, 29, 188] C  tla eU ddF tePd gblD!h!
    Keys  [26, 123, 39, 155, 51] C  uqa eswddFueePdoAbl!Th!
    Keys  [26, 123, 39, 155, 77] C  uda es ddFu!ePdo bl!dh!
    Keys  [26, 123, 39, 155, 188] C  ula es ddFutePdogbl!!h!
    Keys  [26, 123, 39, 218, 51] C  Lqa eswddFeeePdcAbltTh!
    Keys  [26, 123, 39, 218, 77] C  Lda es ddFe!ePdc bltdh!
    Keys  [26, 123, 39, 218, 188] C  Lla es ddFetePdcgblt!h!
    Keys  [26, 123, 180, 29, 51] C ktqa zUwdde eePa Ab DTh
    Keys  [26, 123, 180, 29, 77] C ktda zU dde !ePa  b Ddh
    Keys  [26, 123, 180, 29, 188] C ktla zU dde tePa gb D!h
    Keys  [26, 123, 180, 155, 51] C kuqa zswddeueePaoAb !Th
    Keys  [26, 123, 180, 155, 77] C kuda zs ddeu!ePao b !dh
    Keys  [26, 123, 180, 155, 188] C kula zs ddeutePaogb !!h
    Keys  [26, 123, 180, 218, 51] C kLqa zswddeeeePacAb tTh
    Keys  [26, 123, 180, 218, 77] C kLda zs ddee!ePac b tdh
    Keys  [26, 123, 180, 218, 188] C kLla zs ddeetePacgb t!h
    Keys  [123, 76, 5, 29, 51] Laztqi iUwa c ee d AgoDT
    Keys  [123, 76, 5, 29, 77] Laztdi iU a c !e d  goDd
    Keys  [123, 76, 5, 29, 188] Laztli iU a c te d ggoD!
    Keys  [123, 76, 5, 155, 51] Lazuqi iswa cuee doAgo!T
    Keys  [123, 76, 5, 155, 77] Lazudi is a cu!e do go!d
    Keys  [123, 76, 5, 155, 188] Lazuli is a cute doggo!!
    Keys  [123, 76, 5, 218, 51] LazLqi iswa ceee dcAgotT
    Keys  [123, 76, 5, 218, 77] LazLdi is a ce!e dc gotd
    Keys  [123, 76, 5, 218, 188] LazLli is a cete dcggot!
    Keys  [123, 76, 39, 29, 51] La tqi eUwa F ee d AglDTo!
    Keys  [123, 76, 39, 29, 77] La tdi eU a F !e d  glDdo!
    Keys  [123, 76, 39, 29, 188] La tli eU a F te d gglD!o!
    Keys  [123, 76, 39, 155, 51] La uqi eswa Fuee doAgl!To!
    Keys  [123, 76, 39, 155, 77] La udi es a Fu!e do gl!do!
    Keys  [123, 76, 39, 155, 188] La uli es a Fute doggl!!o!
    Keys  [123, 76, 39, 218, 51] La Lqi eswa Feee dcAgltTo!
    Keys  [123, 76, 39, 218, 77] La Ldi es a Fe!e dc gltdo!
    Keys  [123, 76, 39, 218, 188] La Lli es a Fete dcgglt!o!
    Keys  [123, 76, 180, 29, 51] Laktqi zUwa e ee a Ag DTo
    Keys  [123, 76, 180, 29, 77] Laktdi zU a e !e a  g Ddo
    Keys  [123, 76, 180, 29, 188] Laktli zU a e te a gg D!o
    Keys  [123, 76, 180, 155, 51] Lakuqi zswa euee aoAg !To
    Keys  [123, 76, 180, 155, 77] Lakudi zs a eu!e ao g !do
    Keys  [123, 76, 180, 155, 188] Lakuli zs a eute aogg !!o
    Keys  [123, 76, 180, 218, 51] LakLqi zswa eeee acAg tTo
    Keys  [123, 76, 180, 218, 77] LakLdi zs a ee!e ac g tdo
    Keys  [123, 76, 180, 218, 188] LakLli zs a eete acgg t!o
    Keys  [123, 99, 5, 29, 51] LGztqiwiUwa2c ee d AgaDT
    Keys  [123, 99, 5, 29, 77] LGztdiwiU a2c !e d  gaDd
    Keys  [123, 99, 5, 29, 188] LGztliwiU a2c te d ggaD!
    Keys  [123, 99, 5, 155, 51] LGzuqiwiswa2cuee doAga!T
    Keys  [123, 99, 5, 155, 77] LGzudiwis a2cu!e do ga!d
    Keys  [123, 99, 5, 155, 188] LGzuliwis a2cute dogga!!
    Keys  [123, 99, 5, 218, 51] LGzLqiwiswa2ceee dcAgatT
    Keys  [123, 99, 5, 218, 77] LGzLdiwis a2ce!e dc gatd
    Keys  [123, 99, 5, 218, 188] LGzLliwis a2cete dcggat!
    Keys  [123, 99, 39, 29, 51] LG tqiweUwa2F ee d AglDTa!
    Keys  [123, 99, 39, 29, 77] LG tdiweU a2F !e d  glDda!
    Keys  [123, 99, 39, 29, 188] LG tliweU a2F te d gglD!a!
    Keys  [123, 99, 39, 155, 51] LG uqiweswa2Fuee doAgl!Ta!
    Keys  [123, 99, 39, 155, 77] LG udiwes a2Fu!e do gl!da!
    Keys  [123, 99, 39, 155, 188] LG uliwes a2Fute doggl!!a!
    Keys  [123, 99, 39, 218, 51] LG Lqiweswa2Feee dcAgltTa!
    Keys  [123, 99, 39, 218, 77] LG Ldiwes a2Fe!e dc gltda!
    Keys  [123, 99, 39, 218, 188] LG Lliwes a2Fete dcgglt!a!
    Keys  [123, 99, 180, 29, 51] LGktqiwzUwa2e ee a Ag DTa
    Keys  [123, 99, 180, 29, 77] LGktdiwzU a2e !e a  g Dda
    Keys  [123, 99, 180, 29, 188] LGktliwzU a2e te a gg D!a
    Keys  [123, 99, 180, 155, 51] LGkuqiwzswa2euee aoAg !Ta
    Keys  [123, 99, 180, 155, 77] LGkudiwzs a2eu!e ao g !da
    Keys  [123, 99, 180, 155, 188] LGkuliwzs a2eute aogg !!a
    Keys  [123, 99, 180, 218, 51] LGkLqiwzswa2eeee acAg tTa
    Keys  [123, 99, 180, 218, 77] LGkLdiwzs a2ee!e ac g tda
    Keys  [123, 99, 180, 218, 188] LGkLliwzs a2eete acgg t!a
    Keys  [123, 123, 5, 29, 51] L ztqi iUwadc eePd AghDT
    Keys  [123, 123, 5, 29, 77] L ztdi iU adc !ePd  ghDd
    Keys  [123, 123, 5, 29, 188] L ztli iU adc tePd gghD!
    Keys  [123, 123, 5, 155, 51] L zuqi iswadcueePdoAgh!T
    Keys  [123, 123, 5, 155, 77] L zudi is adcu!ePdo gh!d
    Keys  [123, 123, 5, 155, 188] L zuli is adcutePdoggh!!
    Keys  [123, 123, 5, 218, 51] L zLqi iswadceeePdcAghtT
    Keys  [123, 123, 5, 218, 77] L zLdi is adce!ePdc ghtd
    Keys  [123, 123, 5, 218, 188] L zLli is adcetePdcgght!
    Keys  [123, 123, 39, 29, 51] L  tqi eUwadF eePd AglDTh!
    Keys  [123, 123, 39, 29, 77] L  tdi eU adF !ePd  glDdh!
    Keys  [123, 123, 39, 29, 188] L  tli eU adF tePd gglD!h!
    Keys  [123, 123, 39, 155, 51] L  uqi eswadFueePdoAgl!Th!
    Keys  [123, 123, 39, 155, 77] L  udi es adFu!ePdo gl!dh!
    Keys  [123, 123, 39, 155, 188] L  uli es adFutePdoggl!!h!
    Keys  [123, 123, 39, 218, 51] L  Lqi eswadFeeePdcAgltTh!
    Keys  [123, 123, 39, 218, 77] L  Ldi es adFe!ePdc gltdh!
    Keys  [123, 123, 39, 218, 188] L  Lli es adFetePdcgglt!h!
    Keys  [123, 123, 180, 29, 51] L ktqi zUwade eePa Ag DTh
    Keys  [123, 123, 180, 29, 77] L ktdi zU ade !ePa  g Ddh
    Keys  [123, 123, 180, 29, 188] L ktli zU ade tePa gg D!h
    Keys  [123, 123, 180, 155, 51] L kuqi zswadeueePaoAg !Th
    Keys  [123, 123, 180, 155, 77] L kudi zs adeu!ePao g !dh
    Keys  [123, 123, 180, 155, 188] L kuli zs adeutePaogg !!h
    Keys  [123, 123, 180, 218, 51] L kLqi zswadeeeePacAg tTh
    Keys  [123, 123, 180, 218, 77] L kLdi zs adee!ePac g tdh
    Keys  [123, 123, 180, 218, 188] L kLli zs adeetePacgg t!h
    -> # Run all these combinations through the isEnglish function and print the ones that return True
    In this case the correct key combination should be
    Keys  [123, 76, 5, 155, 188] Lazuli is a cute doggo!!

    """

    # Intalizes lists for the decrypted parts used to decrypt the messages
    decrypted_parts: List[List[int, str]] = [0] * keySize

    # List to store all processes workers
    process_list: List[str] = []

    # A queue to store the result from each process
    queue: Queue = Queue()

    # For each substring of keySize where the subsrting is character of every x*nth + i character where i is the offset of the start of the key
    for i in range(keySize):

        # Collects a subsrting of the text where the subsrting is character of every x*nth + i character where i is the offset of the start of the key
        # This is completed using list comprehension
        sub_text = [text[j] for j in range(len(text)) if j % keySize == i]

        # Spawns a process for each substring of the text
        # The process will be responsible for decrypting (by brute-force) that subsection of the text using a single byte XOR
        # It is also passed in its offset from the key (i) and the queue to store the results
        process = Process(
            target=mutiByteKeyBySingleByteXOR, args=([sub_text], i, queue)
        )
        process_list.append(process)
        process.start()

    # Join all the processes togtether once they have completed
    # Collects the results from the queue deposited by each process and stores them in the decrypted_parts list
    for process in process_list:
        process.join()
        element = queue.get()  # Collect the result fronm the queue
        level = element[0]  # See which part of the text it is (offset from the key)
        decrypted_parts[level] = element[1]  # Collect the key, text combination pairs

    # Collect the results from each queue
    decrypted_parts[0] = list(
        filter(MUTI_BYTE_XOR_SUB_STRING_INITAL_FILTER, decrypted_parts[0])
    )
    decrypted_parts = list(map(MUTI_BYTE_XOR_SUB_STRING_FILTER, decrypted_parts))
    # for items in constructStrings(decrypted_parts)
    #   if isEnglish(items[1]):
    #     print("Correct key: ", decrypted_parts[0][0])
    #     print("Decrypted text: ", decrypted_parts[0][1])
    result = constructStrings(decrypted_parts)
    for item in result:
        print(item, "\n", "\n")
    # for result in constructStrings(decrypted_parts):
    #     print(result, "\n", "\n")


# -- Main -- #


def main():

    # Task 2A
    print("Task 2B\n", "-" * 20, "\n")
    for result in singleXORCracker(
        fileReaderHex("./encrypted_files/Lab0.TaskII.B.txt"), SINGLE_BYTE_XOR_KEY_FILTER
    ):
        print(f"Key: {result[0]}, Text: {result[1][0]}\n{" - "*20}\n")

    # Task 2B
    lab1_taskb_text = fileReaderBase64("./encrypted_files/Lab0.TaskII.C.txt")
    best_key_size = mutiByteXORKeySearch(lab1_taskb_text)
    # print("Best key size: ", best_key_size)
    decryptMutliByteXOR(lab1_taskb_text, 5)


if __name__ == "__main__":
    main()
