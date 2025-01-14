from tools import *
from typing import List
from multiprocessing import Queue, Process
from statistics import mean


def fileReaderHex(file: str) -> List[bytes]:
    with open(file, "r") as f:  # Opens the file in read mode
        lines = f.readlines()  # Reads in all the lines of the file
        texts = []
        for line in lines:  # Loops through each line in the file
            texts.append(
                bytes.fromhex(line.strip())
            )  # Converts the line from a hex string to bytes and appends it to the texts list
    return texts


# the following function reads in a file in base64 encoding and returns a list of bytes encoded as ASCII characters
# The ASCII characters may or may not be printable
def fileReaderBase64(file: str) -> List[bytes]:
    with open(file, "r") as f:  # Opens the file as f in read only mode
        text = f.read().strip("\n")  # Removes all the new line characters from the text
    return base64_to_ascii(
        text
    )  # Converts the base64 encoded text to ASCII characters in byte format


# The following function performs a single byte XOR on a list of text and a key
def singleXORHelperLooper(texts: List[bytes]) -> None:
    # For all possible keys for a single byte XOR
    # for(int key = 0; key < 256; key++)
    for key in range(256):
        singleXORHelper(texts, int.to_bytes(key, 1))


# The following function performs a single byte XOR on a text and a key
def singleXORHelperLooper2(text: bytes) -> float:
    # Creates a list of the index of coincidence values for all possible keys
    indexCoincidenceKeys = []
    # For each possible key in a single byte XOR of a given length
    # For every possible key in a single byte XOR; for(int key = 0; key < 256; key++)
    for key in range(256):
        # Calcilate the index of coincidence for the text after a using that key to decrypt those characters
        # Append that value to the indexCoincidenceKeys list;
        # indexCoincidenceKeys.add(Math.abs(new String(indexCoincidence(implementXOR(text,
        # key.byteValue())),StandardCharsets.UTF_8) - 1.7)
        indexCoincidenceKeys.append(
            abs(
                indexCoincidence(
                    implementXOR(text, int.to_bytes(key, 1)).decode(errors="ignore")
                )
                - 1.7
            )
        )
    # Calculate the mean of all the index of coincidence values
    # indexCoincidenceKeys.stream().mapToDouble(a -> a).average().getAsDouble()
    return mean(indexCoincidenceKeys)


def singleXORHelper(texts: List[bytes], key: bytes) -> List[bytes]:
    extracted_text: List[bytes] = []
    for text in texts:
        extracted_text.append(implementXOR(text, key))  # 0x610x650xF6 --> "Ae.."
    english_text = []
    for text in extracted_text:
        if isEnglish(text.decode(errors="ignore")):
            english_text.append(text.decode(errors="ignore"))
    if len(english_text) > 0:
        print("Key: ", int(hex(key[0]), 16))
        print("Possible ", english_text)


def mutiByteXORHelper(text: bytes, keySize: int, queue: Queue) -> None:
    sub_text = [
        text[i] for i in range(len(text)) if i % keySize == 0
    ]  # Grabs the nth character in a ASCII string if n is a mutiple of the keySize
    queue.put([keySize, singleXORHelperLooper2(sub_text)])


# The following function finds the ideal key size
# fo the mutibyte XOR by minimuzing the index of coincidence difference from ideal English (1.7 )
def mutiByteXOR(text: bytes) -> None:
    q: Queue = Queue()  # Creates a queue for muutiprocessing; Queue q = new Queue()
    process_list: List[Process] = (
        []
    )  # Creates a list to store all processes; List<Process> process_list = new ArrayList<>()
    # Creates a list to store all index of coincidence values and their respective key sizes; List<List<int, int>> indexCoincidenceValues = new ArrayList<>()
    indexCoincidenceValues: List[List[int, float]] = []
    # For all key sizes between 1 and 20 ; for(int i = 1; i < 20; i++)
    for i in range(1, 20):
        # Create a process for each key size ; Process process = new Process(mutiByteXORHelper, text, i, q)
        process = Process(target=mutiByteXORHelper, args=(text, i, q))
        # Append the key size to the process list ; process_list.add(process)
        process_list.append(process)
        # Starts the process ; process.start()
        process.start()
    # Wait for all processes to complete
    for p in process_list:
        # For each process wait for it to complete Then call p.join() ti a; p.join()
        p.join()
    # Retrieve results from all child processes
    # While the queue is not empty ; while(!q.empty())
    while not q.empty():
        # Collect the result and append it to the indexCoincidenceValues list ; indexCoincidenceValues.add(q.get())
        indexCoincidenceValues.append(q.get())
    # Sort the indexCoincidenceValues list by the index of coincidence value ;
    # indexCoincidenceValues.sort((a, b) -> if (a[1] > b[1]) return 1; else if (a[1] < b[1]) return -1; else return 0)
    indexCoincidenceValues.sort(key=lambda x: x[1])
    print(
        indexCoincidenceValues
    )  # Print the indexCoincidenceValues list; System.out.println(indexCoincidenceValues)


def main():
    singleXORHelperLooper(fileReaderHex("Lab0.TaskII.B.txt"))
    lab1_taskb_text = fileReaderBase64(
        "/Users/tigerplayspc/Documents/CS/CSC323/lab0/lab0_b_2.txt"
    )
    mutiByteXOR(lab1_taskb_text)


if __name__ == "__main__":
    main()
