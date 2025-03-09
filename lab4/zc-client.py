import sys, time, json, os
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from transaction import *
from mining import mine
from threading import Thread, Lock

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

    blockChainSize = 1

    utx = []

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(ZachCoinClient, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)

    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        # print("node_message from " + connected_node.id + ": " + json.dumps(data,indent=2))
        print("node_message from " + connected_node.id)

        if data != None:
            if "type" in data:
                print("Received data of type: ", data["type"])
                if data["type"] == self.TRANSACTION:
                    self.utx.append(data)
                    self.send_to_node(data)
                elif data["type"] == self.BLOCKCHAIN:
                    self.blockchain = data["blockchain"]
                    self.wallet, self.balance = calculateUserBalance(
                        self.blockchain, self.sk
                    )
                    self.blockChainSize = len(self.blockchain)
                elif data["type"] == self.UTXPOOL:
                    self.utx = data["utxpool"]
                elif data["type"] == self.BLOCK:
                    if verifyBlock(self.blockchain, data):
                        self.blockchain.append(data)

                        # Remove from utxpool
                        for utx in self.utx:
                            if (
                                utx["input"]["id"] == data["tx"]["input"]["id"]
                                and utx["input"]["n"] == data["tx"]["input"]["n"]
                            ):
                                self.utx.remove(utx)
                                break

                        self.wallet, self.balance = calculateUserBalance(
                            self.blockchain, self.sk
                        )
                        self.blockChainSize += 1
                        print("Block added to blockchain")

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)

    def node_request_to_stop(self):
        print("node is requested to stop!")


def newTransaction(client, sk):
    os.system("cls" if os.name == "nt" else "clear")
    print(f'{"="*30} New Transaction {"="*30}')

    while True:
        try:
            to = input("Enter the recipient's public key: ")
            amount = int(input("Enter the amount to send: "))
            break
        except ValueError:
            print("Error: Invalid input.")
    input(
        "Confirm?\n\tTo: "
        + to
        + "\n\tAmount: "
        + str(amount)
        + "\n\tPress Enter to confirm"
    )
    try:
        transaction = createTransaction(client.wallet, client.balance, sk, amount, to)
        client.utx.append(transaction)
        client.semd_to_nodes(transaction)
    except Exception as Errro:
        print("", "=" * 30, "\n", Errro, "\n", "=" * 30)
        input()


def main():

    # if len(sys.argv) < 3:
    #     print("Usage: python3", sys.argv[0], "CLIENTNAME PORT")
    #     quit()

    sys.argv = ["zc-client.py", "bkwong01", "9067"]

    # Load keys, or create them if they do not yet exist
    keypath = "./" + sys.argv[1] + ".key"
    if not os.path.exists(keypath):
        sk = SigningKey.generate()
        vk = sk.verifying_key
        with open(keypath, "w") as f:
            f.write(sk.to_string().hex())
            f.close()
    else:
        with open(keypath) as f:
            try:
                sk = SigningKey.from_string(bytes.fromhex(f.read()))
                vk = sk.verifying_key
            except Exception as e:
                print("Couldn't read key file", e)

    # Create a client object
    client = ZachCoinClient("127.0.0.1", int(sys.argv[2]), sys.argv[1])
    client.sk = sk
    client.pk = vk
    client.debug = False

    time.sleep(1)

    client.start()

    time.sleep(1)

    # Connect to server
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    print("Starting ZachCoin™ Client:", sys.argv[1])
    time.sleep(2)

    mine_thread = None
    mine_lock = Lock()

    while True:
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
            "\t0: Print keys\n\t1: Print blockchain\n\t2: Print UTX pool\n\t3: New Transaction\n\t4: Mine Zackcoin\n\t5. Exit\n\nEnter your choice -> "
        )
        try:
            x = int(x)
        except:
            print("Error: Invalid menu option.")
            input()
            continue
        if x == 0:
            print("sk: ", sk.to_string().hex())
            print("vk: ", vk.to_string().hex())
        elif x == 1:
            print(json.dumps(client.blockchain, indent=1))
        elif x == 2:
            print(json.dumps(client.utx, indent=1))
        elif x == 3:
            thread = Thread(target=newTransaction, args=(client, sk))
            thread.start()
            thread.join()
            continue
        elif x == 4:
            if mine_thread is not None:
                print("Mining thread already running\n\t Want to terminate?")
                if input("Enter Y to terminate: ") == "Y":
                    print("Terminating mining thread after this block")
                    mine_lock.release()
                    mine_thread.join()
                    mine_thread = None
            else:
                mine_lock.acquire()
                mine_thread = Thread(target=mine, args=(client, mine_lock))
                mine_thread.start()
                print("Mining thread started")
        elif x == 5:
            print("Exiting ZachCoin™ Client")
            if mine_thread is not None:
                mine_lock.release()
                mine_thread.join()
            client.stop()
            sys.exit(0)
        # TODO: Add options for creating and mining transactions
        # as well as any other additional features

        input()


if __name__ == "__main__":
    main()
