import sys, time, json, os
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from transaction import *
from mining import mine, newBlockArrived, detectGPUSupport
from threading import Thread, Lock
import subprocess

# Server connections constants
SERVER_ADDR = "zachcoin.net"
SERVER_PORT = 9067


class ZachCoinClient(Node):

    # ZachCoin Constants
    BLOCK = 0
    TRANSACTION = 1
    BLOCKCHAIN = 2
    UTXPOOL = 3
    COINBASE = 50
    DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    balance = 0
    wallet = None

    sk = None
    pk = None

    # Indicates if the user's computer has GPU acceleration for mining
    hasGPU = False

    # Array used to store the blockchain of ZachCoin
    # Hardcoded gensis block
    blockchain = [
        {
            "type": BLOCK,
            "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
            "nonce": "1950b006f9203221515467fe14765720",
            "pow": "00000027e2eb250f341b05ffe24f43adae3b8181739cd976ea263a4ae0ff8eb7",
            "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
            "tx": {
                "type": TRANSACTION,
                "input": {
                    "id": "0000000000000000000000000000000000000000000000000000000000000000",
                    "n": 0,
                },
                "sig": "adf494f10d30814fd26c6f0e1b2893d0fb3d037b341210bf23ef9705479c7e90879f794a29960d3ff13b50ecd780c872",
                "output": [
                    {
                        "value": 50,
                        "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                    }
                ],
            },
        }
    ]

    # Keeps track of the size of the blockchain
    blockChainSize = 1

    # Array used to store unverified transactions
    utx = []

    # Initializes the client node object

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(ZachCoinClient, self).__init__(host, port, id, callback, max_connections)

    # Node functions used for debugging

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)

    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        """
        The following function parses incoming messages from the network
        and calls the appropriate functions to handle the message.

        :param connected_node: The node that sent the message
        :param data: The message sent by the node

        :return: None
        """

        print("node_message from " + connected_node.id)

        # If there is data in the message
        if data != None:
            # And there is a valid type feild in the message
            if "type" in data:

                # If the incoming message is a transaction
                if data["type"] == self.TRANSACTION:
                    # Add the transaction to the unverified transaction pool
                    self.utx.append(data)
                # If the incoming message is the entire blockchain
                # Only occurs during initial connection
                elif data["type"] == self.BLOCKCHAIN:

                    # Set the blockchain to the incoming blockchain
                    self.blockchain = data["blockchain"]

                    # Recalculate the user's balance and wallet from the new blockchain
                    self.wallet, self.balance = calculateUserBalance(
                        self.blockchain, self.sk
                    )

                    # Set the blockchain size to the length of the new blockchain
                    self.blockChainSize = len(self.blockchain)

                # If the incoming message is the entire UTX pool
                elif data["type"] == self.UTXPOOL:
                    # Set the UTX pool to the incoming UTX pool
                    self.utx = data["utxpool"]

                # If the incoming message is a block
                elif data["type"] == self.BLOCK:

                    # Read in the global newBlockArrived lock
                    global newBlockArrived

                    # Set the newBlockArrived flag to True
                    newBlockArrived = True

                    # Verify the block
                    if verifyBlock(self.blockchain, data):
                        self.blockchain.append(data)
                        # Remove the block's transactions from the UTX pool
                        for utx in self.utx:
                            if (
                                utx["input"]["id"] == data["tx"]["input"]["id"]
                                and utx["input"]["n"] == data["tx"]["input"]["n"]
                            ):
                                self.utx.remove(utx)
                                break

                        # Update the user's balance and wallet
                        self.wallet, self.balance = calculateUserBalance(
                            self.blockchain, self.sk
                        )

                        # Increment the blockchain size
                        self.blockChainSize += 1

                        # Turn off the newBlockArrived flag
                        newBlockArrived = False
                    else:
                        # If the new block is invalid, print the invalid block
                        print("Block verification failed", json.dumps(data, indent=2))

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)

    def node_request_to_stop(self):
        print("node is requested to stop!")


def printWallet(client: ZachCoinClient):
    """

    The following function prints the user's wallet and balance.

    :param client: The ZachCoinClient object

    :return: None
    """

    # Header
    print("=" * 30, "Wallet", "=" * 30)

    # For each entry in the user's wallet
    for entry in client.wallet:
        # Print the block id
        print("Block Id", entry[:-1])
        # Print the index of the transaction in the block being referenced
        print("Index: ", entry[-1])
        # Print the amount of ZachCoin in the block available to the user
        print("Amount: ", client.wallet[entry]["amount"])
        print("-" * 70)
    # Print the accumulated balance of the user
    print("Balance: ", client.balance)


def newTranactionGUI(client: ZachCoinClient, sk: SigningKey):
    """

    The following function is a interface for creating a new transaction.
    It asks for the amount and recipient's public key.
    It then validates those inputs before passing them onto newTransaction function.


    :param client: The ZachCoinClient object
    :param sk: The user's signing key (private key)

    :return: None
    """

    # Clears the screen
    os.system("cls" if os.name == "nt" else "clear")

    # Prints the user's balance
    print(" Balance: ", client.balance)
    print(f'{"="*30} New Transaction {"="*30}')
    # Loops until the user enters valid input
    while True:
        try:
            # Asks for the recipient's public key
            to = input("Enter the recipient's public key: ")
            # Asks for the amount to
            amount = int(input("Enter the amount to send: "))

            # Asks them to confirm the transaction
            input(
                "Confirm?\n\tTo: "
                + to
                + "\n\tAmount: "
                + str(amount)
                + "\n\tPress Enter to confirm"
            )
            newTransaction(client, sk, to, amount)
            break
        # If the user enters invalid input
        # Try again
        except ValueError:
            print("Error: Invalid input.")


def main():
    """
    This function acts as the main thread for the ZachCoin™ client.
    It initializes the client object and connects to the server.
    It then enters an continuous loop that allows the user to interact with the client, dispatching wok to other threads as needed.

    """

    # Validate command line arguments
    if len(sys.argv) < 3:
        print("Usage: python3", sys.argv[0], "CLIENTNAME PORT")
        quit()

    # Load keys, or create them if they do not yet exist
    keypath = "./" + sys.argv[1] + ".key"
    if not os.path.exists(keypath):
        sk = SigningKey.generate()
        vk = sk.verifying_key
        with open(keypath, "w") as f:
            f.write(sk.to_string().hex())
            f.close()
    # Of keys are found, load them in from the file
    else:
        with open(keypath) as f:
            try:
                sk = SigningKey.from_string(bytes.fromhex(f.read()))
                vk = sk.verifying_key
            except Exception as e:
                print("Couldn't read key file", e)

    # Create a client object
    client = ZachCoinClient("127.0.0.1", int(sys.argv[2]), sys.argv[1])

    # Set the client's public and private keys
    client.sk = sk
    client.pk = vk
    client.debug = False

    try:
        # Check if the GPU is available and if the necessary libraries are installed
        detectGPUSupport()
        client.hasGPU = True
    except ModuleNotFoundError as e:
        print(e)
        print("Did you make sure to install the GPU dependencies?")
        input("Press enter to continue with CPU mining")
    except Exception as e:
        print(e)
        pass

    # Wait for the client to start
    time.sleep(1)

    client.start()

    # Wait for the client to start up and initialize
    time.sleep(1)

    # Connect to server
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    print("Starting ZachCoin™ Client:", sys.argv[1])
    # Wait for the client to connect to the server
    time.sleep(3)

    # Initialize mining thread as false and creates a lock for the thread
    # Will use as ITC for communication between main thread and mining thread
    mine_thread = None
    mine_lock = Lock()

    # Main menu loop
    while True:
        # Clears the screen and prints available options
        os.system("cls" if os.name == "nt" else "clear")
        slogan = ' You can\'t spell "It\'s a Ponzi scheme!" without "ZachCoin" '
        print(
            "=" * (int(len(slogan) / 2) - int(len(" ZachCoin™") / 2)),
            "ZachCoin™",
            "=" * (int(len(slogan) / 2) - int(len("ZachCoin™ ") / 2)),
        )
        print(slogan)
        print("=" * len(slogan), "\n")
        print("Balance: ", client.balance, "\n")
        x = input(
            "\t0: Print keys\n\t1: Write blockchain\n\t2: Write UTX pool\n\t3: New Transaction\n\t4: Mine Zackcoin\n\t5. Show Wallet\n\t6. Exit\n\nEnter your choice -> "
        )
        try:
            # Collects the user's input
            x = int(x)
        except:
            # If the user enters invalid input
            # Try again
            print("Error: Invalid menu option.")
            input()
            continue

        # If the user selected 0, print their keys
        if x == 0:
            # Convert the keys to hex and print them
            print("sk: ", sk.to_string().hex())
            print("vk: ", vk.to_string().hex())
        # If the user selected 1, write the blockchain to blockchain.json
        elif x == 1:
            # Open or create the blockchain.json file
            with open("blockchain.json", "w") as f:
                # Write the blockchain to the file
                f.write(json.dumps(client.blockchain, indent=1))
            print("Blockchain written to blockchain.json")
        # If the user selected 2, write the UTX pool to utxpool.json
        elif x == 2:
            with open("utxpool.json", "w") as f:
                f.write(json.dumps(client.utx, indent=1))
            print("UTX pool written to utxpool.json")
        # If the user selected 3, create a new transaction
        elif x == 3:
            # Creates and starts a new thread for handling new transaction GUI
            thread = Thread(target=newTranactionGUI, args=(client, sk))
            thread.start()
            thread.join()
            continue
        # If the user selected 4, start the mining thread
        elif x == 4:
            # If the mining thread is already running
            if mine_thread is not None:
                # Ask the user if they want to terminate the thread
                print("Mining thread already running\n\t Want to terminate?")
                if input("Enter Y to terminate: ") == "Y":
                    print("Terminating mining thread after this block")
                    # Signal the mining thread to terminate
                    mine_lock.release()
                    # Wait for the thread to terminate
                    mine_thread.join()
                    # Clears the mining thread
                    mine_thread = None
            else:
                # Else, start the mining thread
                # Ask the user if they want to use GPU mining if supported
                gpu = "N"
                if client.hasGPU:
                    gpu = input("Would you like to use GPU mining? (Y/N): ")

                # Ask the user if they want to auto generate new transactions
                auto = input(
                    "Would you like to auto generate new transactions if the UTX pool is empty for 30 seconds ? (Y/N): "
                )

                # Enable the mining thread to run
                mine_lock.acquire()
                mine_thread = Thread(
                    target=mine,
                    args=(
                        client,
                        mine_lock,
                        gpu == "Y" or gpu == "y",
                        auto == "Y" or auto == "y",
                    ),
                )
                mine_thread.start()
                print("Mining thread started")
        # If the user selected 5, print the user's wallet
        elif x == 5:
            # Call the printWallet function
            printWallet(client)
        # Finally, if the user selected 6, exit the client
        elif x == 6:
            print("Exiting ZachCoin™ Client")
            # If the mining thread is running, terminate it
            if mine_thread is not None:
                mine_lock.release()
                mine_thread.join()
            # Disconnect the client from the server node
            client.stop()
            # Exit the client
            sys.exit(0)
        input()


if __name__ == "__main__":
    main()
