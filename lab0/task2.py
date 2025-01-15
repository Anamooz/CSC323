from tools import *
from typing import List, Tuple
from multiprocessing import Queue, Process
from statistics import mean


# The following function reads in a file of hex encoded strings and converts them into ASCII bytes
def fileReaderHex(file: str) -> List[bytes]:
    with open(file, "r") as f:  # Opens the file in read mode
        lines: List[str] = f.readlines()  # Reads in all the lines of the file
        texts: List[str] = []
        for line in lines:  # Loops through each line in the file
            texts.append(
                bytes.fromhex(line.strip())
            )  # Converts the line from a hex string to bytes and appends it to the texts list
    return texts


# The following function reads in a file in base64 encoding and
# returns a list of bytes encoded as ASCII characters
# The ASCII characters may or may not be printable
def fileReaderBase64(file: str) -> List[bytes]:
    with open(
        file, "r"
    ) as f:  # Opens the file as f in read only mode ; BufferedReader f = new BufferedReader(new FileReader(file))
        text: List[str] = f.read().strip(
            "\n"
        )  # Removes all the new line characters from the text ; ArrayList<String> text = new ArrayList<>(Arrays.asList(f.read().split("\n")))
    return base64_to_ascii(
        text
    )  # Converts the base64 encoded text to ASCII characters in byte format ; Decoder decoder = Base64.getDecoder(); return decoder.decode(text)


# The following function performs a single byte XOR on a list of text and a key
def singleXORHelperLooper(texts: List[bytes]) -> List[Tuple[int, str]]:
    # For all possible keys for a single byte XOR
    # for(int key = 0; key < 256; key++)
    possible_keys_texts: List[Tuple[int, str]] = []
    for key in range(256):
        # k : is the key used to decrypt the text
        # string : is the decrypted text
        k, string = singleXORHelper(texts, int.to_bytes(key, 1))
        if string is not None:  # If there is a match
            possible_keys_texts.append(
                (k, string)
            )  # Add the key and the text to the list of possible keys text combinations
    return possible_keys_texts  # Return the list of possible keys text combinations


# The following function brute forces a single byte XOR on a list of text and a key
# It then calculates the average [mean] difference index of coincidence for the decrypted text compared to the IC of English (1.7)
# A lower difference index of coincidence value indicates that the text is more likely to be English
def singleXORIndexOfCoincidenceCalculator(text: bytes) -> float:
    # Creates a list of the index of coincidence values for all possible keys
    # ArrayList<Float> indexCoincidenceKeys = new ArrayList<>()
    indexCoincidenceKeys: List[float] = []
    # For each possible key in a single byte XOR of a given length
    # For every possible key in a single byte XOR; for(int key = 0; key < 256; key++)
    # for(int key = 0; key < 256; key++)
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


# The following function performs a single byte XOR on a text and a key
# It will return all keys that are possible texts in English along with their assiocated text
# Return type will be of type list of tuples where the first element is the key and the second element is the text of a match is foound or
# key, None oyherwise
def singleXORHelper(texts: List[bytes], key: bytes) -> List[bytes]:
    extracted_text: List[bytes] = []
    for text in texts:
        extracted_text.append(implementXOR(text, key))  # 0x610x650xF6 --> "Ae.."
    english_text = []
    for text in extracted_text:
        if isEnglish(text.decode(errors="ignore")):
            english_text.append(text.decode(errors="ignore"))
    if len(english_text) > 0:
        return (int(hex(key[0]), 16), english_text)
    else:
        return (int(hex(key[0]), 16), None)


# The following function splits the string only extracting the xth character where x is a multiple of the key size
# Ex if the key size is 5 then this function will only test decryption the 5th, 10th, 15th, 20th, ... characters
def mutiByteXORHelper(text: bytes, keySize: int, queue: Queue) -> None:
    sub_text = [
        text[i] for i in range(len(text)) if i % keySize == 0
    ]  # Grabs the nth character in a ASCII string if n is a mutiple of the keySize
    queue.put([keySize, singleXORIndexOfCoincidenceCalculator(sub_text)])


# The following function finds the ideal key size
# fo the mutibyte XOR by minimuzing the index of coincidence difference from ideal English (1.7 )
def mutiByteXORKeySearxh(text: bytes) -> None:
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
    # print(
    #     indexCoincidenceValues
    # )  # Print the indexCoincidenceValues list; System.out.println(indexCoincidenceValues)
    return indexCoincidenceValues[0][
        0
    ]  # Return the key size with the smallest index of coincidence value ; return indexCoincidenceValues.get(0).get(0)


# The following function decrtypes a mutibyte XOR encrypted text guven a key size of N bytes
# The function will use mutiple processes each responsible for decrypting part of the text
# The results will then be joined together to form the final decrypted text or texts
def decipherMutliByteXOR(text: bytes, keySize: int) -> None:
    # Intalizes lists for the decrypted parts and the processes used to decrypt the messages
    decrypted_parts: List[str] = []
    # List to store all processes
    process_list: List[str] = []
    queue: Queue = Queue()  # A queue to store the result from each process
    for i in range(keySize):
        sub_text = [text[i] for j in range(len(text)) if j % keySize == i]
        process = Process(target=singleXORHelperLooper, args=([sub_text],))
        process.append(process)
        process.start()
    # Join all the processes togtether once they have completed
    for process in process_list:
        process.join()
    # To be done ...
    # Collect the results from each queue
    # Match the each part of the text with the correct key
    # Make a list of all different combvinations
    # For instance given a key size of 5 and 3 results form each process decrypted_parts could look like
    # decrypted_parts[0] = [[15, "aZcde"], [26, "Cadeb"], [123, "Liaeg"]]
    # decrppted_parts[1] = [[76, "a   o"], [99, "Gw2 a"], [123, "  dPh"]]
    # decrypted_parts[2] = [[5, "zicd"], [39, " eFdl!"], [180, "kzea "]]
    # decrypted_parts[3] = [[29, "tU  D"], [155, "usuo!"], [218, "Lsect"]]
    # decrypted_parts[4] = [[51, "qweAT"], [77,"d ! d"], [188, "l tg!"]]
    # which would provide the following combinations
    # Keys  [15, 76, 5, 29, 51] aaztqZ iUwc c ed d AeoDT
    # Keys  [15, 76, 5, 29, 77] aaztdZ iU c c !d d  eoDd
    # Keys  [15, 76, 5, 29, 188] aaztlZ iU c c td d geoD!
    # Keys  [15, 76, 5, 155, 51] aazuqZ iswc cued doAeo!T
    # Keys  [15, 76, 5, 155, 77] aazudZ is c cu!d do eo!d
    # Keys  [15, 76, 5, 155, 188] aazulZ is c cutd dogeo!!
    # Keys  [15, 76, 5, 218, 51] aazLqZ iswc ceed dcAeotT
    # Keys  [15, 76, 5, 218, 77] aazLdZ is c ce!d dc eotd
    # Keys  [15, 76, 5, 218, 188] aazLlZ is c cetd dcgeot!
    # Keys  [15, 76, 39, 29, 51] aa tqZ eUwc F ed d AelDTo!
    # Keys  [15, 76, 39, 29, 77] aa tdZ eU c F !d d  elDdo!
    # Keys  [15, 76, 39, 29, 188] aa tlZ eU c F td d gelD!o!
    # Keys  [15, 76, 39, 155, 51] aa uqZ eswc Fued doAel!To!
    # Keys  [15, 76, 39, 155, 77] aa udZ es c Fu!d do el!do!
    # Keys  [15, 76, 39, 155, 188] aa ulZ es c Futd dogel!!o!
    # Keys  [15, 76, 39, 218, 51] aa LqZ eswc Feed dcAeltTo!
    # Keys  [15, 76, 39, 218, 77] aa LdZ es c Fe!d dc eltdo!
    # Keys  [15, 76, 39, 218, 188] aa LlZ es c Fetd dcgelt!o!
    # Keys  [15, 76, 180, 29, 51] aaktqZ zUwc e ed a Ae DTo
    # Keys  [15, 76, 180, 29, 77] aaktdZ zU c e !d a  e Ddo
    # Keys  [15, 76, 180, 29, 188] aaktlZ zU c e td a ge D!o
    # Keys  [15, 76, 180, 155, 51] aakuqZ zswc eued aoAe !To
    # Keys  [15, 76, 180, 155, 77] aakudZ zs c eu!d ao e !do
    # Keys  [15, 76, 180, 155, 188] aakulZ zs c eutd aoge !!o
    # Keys  [15, 76, 180, 218, 51] aakLqZ zswc eeed acAe tTo
    # Keys  [15, 76, 180, 218, 77] aakLdZ zs c ee!d ac e tdo
    # Keys  [15, 76, 180, 218, 188] aakLlZ zs c eetd acge t!o
    # Keys  [15, 99, 5, 29, 51] aGztqZwiUwc2c ed d AeaDT
    # Keys  [15, 99, 5, 29, 77] aGztdZwiU c2c !d d  eaDd
    # Keys  [15, 99, 5, 29, 188] aGztlZwiU c2c td d geaD!
    # Keys  [15, 99, 5, 155, 51] aGzuqZwiswc2cued doAea!T
    # Keys  [15, 99, 5, 155, 77] aGzudZwis c2cu!d do ea!d
    # Keys  [15, 99, 5, 155, 188] aGzulZwis c2cutd dogea!!
    # Keys  [15, 99, 5, 218, 51] aGzLqZwiswc2ceed dcAeatT
    # Keys  [15, 99, 5, 218, 77] aGzLdZwis c2ce!d dc eatd
    # Keys  [15, 99, 5, 218, 188] aGzLlZwis c2cetd dcgeat!
    # Keys  [15, 99, 39, 29, 51] aG tqZweUwc2F ed d AelDTa!
    # Keys  [15, 99, 39, 29, 77] aG tdZweU c2F !d d  elDda!
    # Keys  [15, 99, 39, 29, 188] aG tlZweU c2F td d gelD!a!
    # Keys  [15, 99, 39, 155, 51] aG uqZweswc2Fued doAel!Ta!
    # Keys  [15, 99, 39, 155, 77] aG udZwes c2Fu!d do el!da!
    # Keys  [15, 99, 39, 155, 188] aG ulZwes c2Futd dogel!!a!
    # Keys  [15, 99, 39, 218, 51] aG LqZweswc2Feed dcAeltTa!
    # Keys  [15, 99, 39, 218, 77] aG LdZwes c2Fe!d dc eltda!
    # Keys  [15, 99, 39, 218, 188] aG LlZwes c2Fetd dcgelt!a!
    # Keys  [15, 99, 180, 29, 51] aGktqZwzUwc2e ed a Ae DTa
    # Keys  [15, 99, 180, 29, 77] aGktdZwzU c2e !d a  e Dda
    # Keys  [15, 99, 180, 29, 188] aGktlZwzU c2e td a ge D!a
    # Keys  [15, 99, 180, 155, 51] aGkuqZwzswc2eued aoAe !Ta
    # Keys  [15, 99, 180, 155, 77] aGkudZwzs c2eu!d ao e !da
    # Keys  [15, 99, 180, 155, 188] aGkulZwzs c2eutd aoge !!a
    # Keys  [15, 99, 180, 218, 51] aGkLqZwzswc2eeed acAe tTa
    # Keys  [15, 99, 180, 218, 77] aGkLdZwzs c2ee!d ac e tda
    # Keys  [15, 99, 180, 218, 188] aGkLlZwzs c2eetd acge t!a
    # Keys  [15, 123, 5, 29, 51] a ztqZ iUwcdc edPd AehDT
    # Keys  [15, 123, 5, 29, 77] a ztdZ iU cdc !dPd  ehDd
    # Keys  [15, 123, 5, 29, 188] a ztlZ iU cdc tdPd gehD!
    # Keys  [15, 123, 5, 155, 51] a zuqZ iswcdcuedPdoAeh!T
    # Keys  [15, 123, 5, 155, 77] a zudZ is cdcu!dPdo eh!d
    # Keys  [15, 123, 5, 155, 188] a zulZ is cdcutdPdogeh!!
    # Keys  [15, 123, 5, 218, 51] a zLqZ iswcdceedPdcAehtT
    # Keys  [15, 123, 5, 218, 77] a zLdZ is cdce!dPdc ehtd
    # Keys  [15, 123, 5, 218, 188] a zLlZ is cdcetdPdcgeht!
    # Keys  [15, 123, 39, 29, 51] a  tqZ eUwcdF edPd AelDTh!
    # Keys  [15, 123, 39, 29, 77] a  tdZ eU cdF !dPd  elDdh!
    # Keys  [15, 123, 39, 29, 188] a  tlZ eU cdF tdPd gelD!h!
    # Keys  [15, 123, 39, 155, 51] a  uqZ eswcdFuedPdoAel!Th!
    # Keys  [15, 123, 39, 155, 77] a  udZ es cdFu!dPdo el!dh!
    # Keys  [15, 123, 39, 155, 188] a  ulZ es cdFutdPdogel!!h!
    # Keys  [15, 123, 39, 218, 51] a  LqZ eswcdFeedPdcAeltTh!
    # Keys  [15, 123, 39, 218, 77] a  LdZ es cdFe!dPdc eltdh!
    # Keys  [15, 123, 39, 218, 188] a  LlZ es cdFetdPdcgelt!h!
    # Keys  [15, 123, 180, 29, 51] a ktqZ zUwcde edPa Ae DTh
    # Keys  [15, 123, 180, 29, 77] a ktdZ zU cde !dPa  e Ddh
    # Keys  [15, 123, 180, 29, 188] a ktlZ zU cde tdPa ge D!h
    # Keys  [15, 123, 180, 155, 51] a kuqZ zswcdeuedPaoAe !Th
    # Keys  [15, 123, 180, 155, 77] a kudZ zs cdeu!dPao e !dh
    # Keys  [15, 123, 180, 155, 188] a kulZ zs cdeutdPaoge !!h
    # Keys  [15, 123, 180, 218, 51] a kLqZ zswcdeeedPacAe tTh
    # Keys  [15, 123, 180, 218, 77] a kLdZ zs cdee!dPac e tdh
    # Keys  [15, 123, 180, 218, 188] a kLlZ zs cdeetdPacge t!h
    # Keys  [26, 76, 5, 29, 51] Caztqa iUwd c ee d AboDT
    # Keys  [26, 76, 5, 29, 77] Caztda iU d c !e d  boDd
    # Keys  [26, 76, 5, 29, 188] Caztla iU d c te d gboD!
    # Keys  [26, 76, 5, 155, 51] Cazuqa iswd cuee doAbo!T
    # Keys  [26, 76, 5, 155, 77] Cazuda is d cu!e do bo!d
    # Keys  [26, 76, 5, 155, 188] Cazula is d cute dogbo!!
    # Keys  [26, 76, 5, 218, 51] CazLqa iswd ceee dcAbotT
    # Keys  [26, 76, 5, 218, 77] CazLda is d ce!e dc botd
    # Keys  [26, 76, 5, 218, 188] CazLla is d cete dcgbot!
    # Keys  [26, 76, 39, 29, 51] Ca tqa eUwd F ee d AblDTo!
    # Keys  [26, 76, 39, 29, 77] Ca tda eU d F !e d  blDdo!
    # Keys  [26, 76, 39, 29, 188] Ca tla eU d F te d gblD!o!
    # Keys  [26, 76, 39, 155, 51] Ca uqa eswd Fuee doAbl!To!
    # Keys  [26, 76, 39, 155, 77] Ca uda es d Fu!e do bl!do!
    # Keys  [26, 76, 39, 155, 188] Ca ula es d Fute dogbl!!o!
    # Keys  [26, 76, 39, 218, 51] Ca Lqa eswd Feee dcAbltTo!
    # Keys  [26, 76, 39, 218, 77] Ca Lda es d Fe!e dc bltdo!
    # Keys  [26, 76, 39, 218, 188] Ca Lla es d Fete dcgblt!o!
    # Keys  [26, 76, 180, 29, 51] Caktqa zUwd e ee a Ab DTo
    # Keys  [26, 76, 180, 29, 77] Caktda zU d e !e a  b Ddo
    # Keys  [26, 76, 180, 29, 188] Caktla zU d e te a gb D!o
    # Keys  [26, 76, 180, 155, 51] Cakuqa zswd euee aoAb !To
    # Keys  [26, 76, 180, 155, 77] Cakuda zs d eu!e ao b !do
    # Keys  [26, 76, 180, 155, 188] Cakula zs d eute aogb !!o
    # Keys  [26, 76, 180, 218, 51] CakLqa zswd eeee acAb tTo
    # Keys  [26, 76, 180, 218, 77] CakLda zs d ee!e ac b tdo
    # Keys  [26, 76, 180, 218, 188] CakLla zs d eete acgb t!o
    # Keys  [26, 99, 5, 29, 51] CGztqawiUwd2c ee d AbaDT
    # Keys  [26, 99, 5, 29, 77] CGztdawiU d2c !e d  baDd
    # Keys  [26, 99, 5, 29, 188] CGztlawiU d2c te d gbaD!
    # Keys  [26, 99, 5, 155, 51] CGzuqawiswd2cuee doAba!T
    # Keys  [26, 99, 5, 155, 77] CGzudawis d2cu!e do ba!d
    # Keys  [26, 99, 5, 155, 188] CGzulawis d2cute dogba!!
    # Keys  [26, 99, 5, 218, 51] CGzLqawiswd2ceee dcAbatT
    # Keys  [26, 99, 5, 218, 77] CGzLdawis d2ce!e dc batd
    # Keys  [26, 99, 5, 218, 188] CGzLlawis d2cete dcgbat!
    # Keys  [26, 99, 39, 29, 51] CG tqaweUwd2F ee d AblDTa!
    # Keys  [26, 99, 39, 29, 77] CG tdaweU d2F !e d  blDda!
    # Keys  [26, 99, 39, 29, 188] CG tlaweU d2F te d gblD!a!
    # Keys  [26, 99, 39, 155, 51] CG uqaweswd2Fuee doAbl!Ta!
    # Keys  [26, 99, 39, 155, 77] CG udawes d2Fu!e do bl!da!
    # Keys  [26, 99, 39, 155, 188] CG ulawes d2Fute dogbl!!a!
    # Keys  [26, 99, 39, 218, 51] CG Lqaweswd2Feee dcAbltTa!
    # Keys  [26, 99, 39, 218, 77] CG Ldawes d2Fe!e dc bltda!
    # Keys  [26, 99, 39, 218, 188] CG Llawes d2Fete dcgblt!a!
    # Keys  [26, 99, 180, 29, 51] CGktqawzUwd2e ee a Ab DTa
    # Keys  [26, 99, 180, 29, 77] CGktdawzU d2e !e a  b Dda
    # Keys  [26, 99, 180, 29, 188] CGktlawzU d2e te a gb D!a
    # Keys  [26, 99, 180, 155, 51] CGkuqawzswd2euee aoAb !Ta
    # Keys  [26, 99, 180, 155, 77] CGkudawzs d2eu!e ao b !da
    # Keys  [26, 99, 180, 155, 188] CGkulawzs d2eute aogb !!a
    # Keys  [26, 99, 180, 218, 51] CGkLqawzswd2eeee acAb tTa
    # Keys  [26, 99, 180, 218, 77] CGkLdawzs d2ee!e ac b tda
    # Keys  [26, 99, 180, 218, 188] CGkLlawzs d2eete acgb t!a
    # Keys  [26, 123, 5, 29, 51] C ztqa iUwddc eePd AbhDT
    # Keys  [26, 123, 5, 29, 77] C ztda iU ddc !ePd  bhDd
    # Keys  [26, 123, 5, 29, 188] C ztla iU ddc tePd gbhD!
    # Keys  [26, 123, 5, 155, 51] C zuqa iswddcueePdoAbh!T
    # Keys  [26, 123, 5, 155, 77] C zuda is ddcu!ePdo bh!d
    # Keys  [26, 123, 5, 155, 188] C zula is ddcutePdogbh!!
    # Keys  [26, 123, 5, 218, 51] C zLqa iswddceeePdcAbhtT
    # Keys  [26, 123, 5, 218, 77] C zLda is ddce!ePdc bhtd
    # Keys  [26, 123, 5, 218, 188] C zLla is ddcetePdcgbht!
    # Keys  [26, 123, 39, 29, 51] C  tqa eUwddF eePd AblDTh!
    # Keys  [26, 123, 39, 29, 77] C  tda eU ddF !ePd  blDdh!
    # Keys  [26, 123, 39, 29, 188] C  tla eU ddF tePd gblD!h!
    # Keys  [26, 123, 39, 155, 51] C  uqa eswddFueePdoAbl!Th!
    # Keys  [26, 123, 39, 155, 77] C  uda es ddFu!ePdo bl!dh!
    # Keys  [26, 123, 39, 155, 188] C  ula es ddFutePdogbl!!h!
    # Keys  [26, 123, 39, 218, 51] C  Lqa eswddFeeePdcAbltTh!
    # Keys  [26, 123, 39, 218, 77] C  Lda es ddFe!ePdc bltdh!
    # Keys  [26, 123, 39, 218, 188] C  Lla es ddFetePdcgblt!h!
    # Keys  [26, 123, 180, 29, 51] C ktqa zUwdde eePa Ab DTh
    # Keys  [26, 123, 180, 29, 77] C ktda zU dde !ePa  b Ddh
    # Keys  [26, 123, 180, 29, 188] C ktla zU dde tePa gb D!h
    # Keys  [26, 123, 180, 155, 51] C kuqa zswddeueePaoAb !Th
    # Keys  [26, 123, 180, 155, 77] C kuda zs ddeu!ePao b !dh
    # Keys  [26, 123, 180, 155, 188] C kula zs ddeutePaogb !!h
    # Keys  [26, 123, 180, 218, 51] C kLqa zswddeeeePacAb tTh
    # Keys  [26, 123, 180, 218, 77] C kLda zs ddee!ePac b tdh
    # Keys  [26, 123, 180, 218, 188] C kLla zs ddeetePacgb t!h
    # Keys  [123, 76, 5, 29, 51] Laztqi iUwa c ee d AgoDT
    # Keys  [123, 76, 5, 29, 77] Laztdi iU a c !e d  goDd
    # Keys  [123, 76, 5, 29, 188] Laztli iU a c te d ggoD!
    # Keys  [123, 76, 5, 155, 51] Lazuqi iswa cuee doAgo!T
    # Keys  [123, 76, 5, 155, 77] Lazudi is a cu!e do go!d
    # Keys  [123, 76, 5, 155, 188] Lazuli is a cute doggo!!
    # Keys  [123, 76, 5, 218, 51] LazLqi iswa ceee dcAgotT
    # Keys  [123, 76, 5, 218, 77] LazLdi is a ce!e dc gotd
    # Keys  [123, 76, 5, 218, 188] LazLli is a cete dcggot!
    # Keys  [123, 76, 39, 29, 51] La tqi eUwa F ee d AglDTo!
    # Keys  [123, 76, 39, 29, 77] La tdi eU a F !e d  glDdo!
    # Keys  [123, 76, 39, 29, 188] La tli eU a F te d gglD!o!
    # Keys  [123, 76, 39, 155, 51] La uqi eswa Fuee doAgl!To!
    # Keys  [123, 76, 39, 155, 77] La udi es a Fu!e do gl!do!
    # Keys  [123, 76, 39, 155, 188] La uli es a Fute doggl!!o!
    # Keys  [123, 76, 39, 218, 51] La Lqi eswa Feee dcAgltTo!
    # Keys  [123, 76, 39, 218, 77] La Ldi es a Fe!e dc gltdo!
    # Keys  [123, 76, 39, 218, 188] La Lli es a Fete dcgglt!o!
    # Keys  [123, 76, 180, 29, 51] Laktqi zUwa e ee a Ag DTo
    # Keys  [123, 76, 180, 29, 77] Laktdi zU a e !e a  g Ddo
    # Keys  [123, 76, 180, 29, 188] Laktli zU a e te a gg D!o
    # Keys  [123, 76, 180, 155, 51] Lakuqi zswa euee aoAg !To
    # Keys  [123, 76, 180, 155, 77] Lakudi zs a eu!e ao g !do
    # Keys  [123, 76, 180, 155, 188] Lakuli zs a eute aogg !!o
    # Keys  [123, 76, 180, 218, 51] LakLqi zswa eeee acAg tTo
    # Keys  [123, 76, 180, 218, 77] LakLdi zs a ee!e ac g tdo
    # Keys  [123, 76, 180, 218, 188] LakLli zs a eete acgg t!o
    # Keys  [123, 99, 5, 29, 51] LGztqiwiUwa2c ee d AgaDT
    # Keys  [123, 99, 5, 29, 77] LGztdiwiU a2c !e d  gaDd
    # Keys  [123, 99, 5, 29, 188] LGztliwiU a2c te d ggaD!
    # Keys  [123, 99, 5, 155, 51] LGzuqiwiswa2cuee doAga!T
    # Keys  [123, 99, 5, 155, 77] LGzudiwis a2cu!e do ga!d
    # Keys  [123, 99, 5, 155, 188] LGzuliwis a2cute dogga!!
    # Keys  [123, 99, 5, 218, 51] LGzLqiwiswa2ceee dcAgatT
    # Keys  [123, 99, 5, 218, 77] LGzLdiwis a2ce!e dc gatd
    # Keys  [123, 99, 5, 218, 188] LGzLliwis a2cete dcggat!
    # Keys  [123, 99, 39, 29, 51] LG tqiweUwa2F ee d AglDTa!
    # Keys  [123, 99, 39, 29, 77] LG tdiweU a2F !e d  glDda!
    # Keys  [123, 99, 39, 29, 188] LG tliweU a2F te d gglD!a!
    # Keys  [123, 99, 39, 155, 51] LG uqiweswa2Fuee doAgl!Ta!
    # Keys  [123, 99, 39, 155, 77] LG udiwes a2Fu!e do gl!da!
    # Keys  [123, 99, 39, 155, 188] LG uliwes a2Fute doggl!!a!
    # Keys  [123, 99, 39, 218, 51] LG Lqiweswa2Feee dcAgltTa!
    # Keys  [123, 99, 39, 218, 77] LG Ldiwes a2Fe!e dc gltda!
    # Keys  [123, 99, 39, 218, 188] LG Lliwes a2Fete dcgglt!a!
    # Keys  [123, 99, 180, 29, 51] LGktqiwzUwa2e ee a Ag DTa
    # Keys  [123, 99, 180, 29, 77] LGktdiwzU a2e !e a  g Dda
    # Keys  [123, 99, 180, 29, 188] LGktliwzU a2e te a gg D!a
    # Keys  [123, 99, 180, 155, 51] LGkuqiwzswa2euee aoAg !Ta
    # Keys  [123, 99, 180, 155, 77] LGkudiwzs a2eu!e ao g !da
    # Keys  [123, 99, 180, 155, 188] LGkuliwzs a2eute aogg !!a
    # Keys  [123, 99, 180, 218, 51] LGkLqiwzswa2eeee acAg tTa
    # Keys  [123, 99, 180, 218, 77] LGkLdiwzs a2ee!e ac g tda
    # Keys  [123, 99, 180, 218, 188] LGkLliwzs a2eete acgg t!a
    # Keys  [123, 123, 5, 29, 51] L ztqi iUwadc eePd AghDT
    # Keys  [123, 123, 5, 29, 77] L ztdi iU adc !ePd  ghDd
    # Keys  [123, 123, 5, 29, 188] L ztli iU adc tePd gghD!
    # Keys  [123, 123, 5, 155, 51] L zuqi iswadcueePdoAgh!T
    # Keys  [123, 123, 5, 155, 77] L zudi is adcu!ePdo gh!d
    # Keys  [123, 123, 5, 155, 188] L zuli is adcutePdoggh!!
    # Keys  [123, 123, 5, 218, 51] L zLqi iswadceeePdcAghtT
    # Keys  [123, 123, 5, 218, 77] L zLdi is adce!ePdc ghtd
    # Keys  [123, 123, 5, 218, 188] L zLli is adcetePdcgght!
    # Keys  [123, 123, 39, 29, 51] L  tqi eUwadF eePd AglDTh!
    # Keys  [123, 123, 39, 29, 77] L  tdi eU adF !ePd  glDdh!
    # Keys  [123, 123, 39, 29, 188] L  tli eU adF tePd gglD!h!
    # Keys  [123, 123, 39, 155, 51] L  uqi eswadFueePdoAgl!Th!
    # Keys  [123, 123, 39, 155, 77] L  udi es adFu!ePdo gl!dh!
    # Keys  [123, 123, 39, 155, 188] L  uli es adFutePdoggl!!h!
    # Keys  [123, 123, 39, 218, 51] L  Lqi eswadFeeePdcAgltTh!
    # Keys  [123, 123, 39, 218, 77] L  Ldi es adFe!ePdc gltdh!
    # Keys  [123, 123, 39, 218, 188] L  Lli es adFetePdcgglt!h!
    # Keys  [123, 123, 180, 29, 51] L ktqi zUwade eePa Ag DTh
    # Keys  [123, 123, 180, 29, 77] L ktdi zU ade !ePa  g Ddh
    # Keys  [123, 123, 180, 29, 188] L ktli zU ade tePa gg D!h
    # Keys  [123, 123, 180, 155, 51] L kuqi zswadeueePaoAg !Th
    # Keys  [123, 123, 180, 155, 77] L kudi zs adeu!ePao g !dh
    # Keys  [123, 123, 180, 155, 188] L kuli zs adeutePaogg !!h
    # Keys  [123, 123, 180, 218, 51] L kLqi zswadeeeePacAg tTh
    # Keys  [123, 123, 180, 218, 77] L kLdi zs adee!ePac g tdh
    # Keys  [123, 123, 180, 218, 188] L kLli zs adeetePacgg t!h
    # -> # Run all these combinations through the isEnglish function and print the ones that return True
    # In this case the correct key combination should be
    # Keys  [123, 76, 5, 155, 188] Lazuli is a cute doggo!!


def main():
    for result in singleXORHelperLooper(fileReaderHex("Lab0.TaskII.B.txt")):
        print(result)
    lab1_taskb_text = fileReaderBase64("lab0_b_2.txt")
    best_key_size = mutiByteXORKeySearxh(lab1_taskb_text)
    print("Best key size: ", best_key_size)


if __name__ == "__main__":
    main()
