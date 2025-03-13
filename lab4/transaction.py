from ecdsa import VerifyingKey, SigningKey
import json
import hashlib
from typing import List

# Dofficulty of the blockchain to mine a block
# Approx 1 in 1/2^255 chance of mining a block ~ 1/33554432
DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def newTransaction(client, sk: SigningKey, to: str, amount: int) -> None:
    """
    The following function creates a new tranaction for a client given their secret key, the recipient's public key, and the amount of coins to be sent.
    Balance is first calculated and then the transaction is created and sent to the nodes.

    :param client: The client object (zc-client.py)
    :param sk: The secret key of the client (ecdsa.SigningKey)
    :param to: The public key of the recipient (in hex string)
    :param amount: The amount of coins to be sent (int)

    :return: None
    """

    try:

        # Updates the user wallet and balance for the latest in the blockchain
        # Only tranactions in the blockchain can be used for new transactions
        client.wallet, client.balance = calculateUserBalance(
            client.blockchain, client.sk
        )

        # Calls the create transaction function to create a new transaction
        transaction = createTransaction(client.wallet, client.balance, sk, amount, to)

        # Briadcast the transaction to the nodes
        client.send_to_nodes(transaction)
    except Exception as Errro:

        # If an error alert that a transaction could not be created
        print("Failed to create transaction: ", Errro)


def verifySignature(transaction: dict, pubKey: str, fromChain: bool = False) -> bool:
    """
    The following function verifies the signature of a transaction given the transaction, and the puiblic key of the sender.
    It returns true if the signature is valid, and false otherwise.

    The signiture covers the input and output of the transaction not counting the coinbase (last transaction).


    :param transaction: The transaction to be verified (dict)
    :param pubKey: The public key of the sender (in hex string)
    :param fromChain: If the transaction is from the blockchain (bool).  By default False

    :return: True if the signature is valid, False otherwise
    """

    try:

        # If from the blockchain, remove the coin base or last transaction
        coreTranaction = transaction["output"]
        if fromChain:
            coreTranaction = transaction["output"][:-1]

        # Extract the signature and the message from the transaction
        signature = bytes.fromhex(transaction["sig"])

        # Gets the input and output of the transaction
        message = json.dumps(transaction["input"], sort_keys=True).encode(
            "utf8"
        ) + json.dumps(coreTranaction, sort_keys=True).encode("utf8")

        # Create Verify Key
        vk = VerifyingKey.from_string(bytes.fromhex(pubKey))
        # Verify the signature
        return vk.verify(signature, message)
    except Exception as e:
        # An exception is thrown if the signature is invalid
        return False


def signTransaction(transaction: dict, privKey: SigningKey) -> str:
    """
    The following function signs a transaction given the transaction and a private key of the sender.
    The signiture covers the input and output of the transaction not counting the coinbase (last transaction).

    :param transaction: The transaction to be signed (dict)
    :param privKey: The private key of the sender (ecdsa.SigningKey)

    :return: The signature of the transaction (in hex string)
    """

    # Get the message to be signed
    message = json.dumps(transaction["input"], sort_keys=True).encode(
        "utf8"
    ) + json.dumps(transaction["output"][:2], sort_keys=True).encode("utf8")

    # Sign the message
    signature = privKey.sign(message)

    # Return the signature in hex
    return signature.hex()


def verify(blockchain: List[dict], transaction: dict, mined: bool = False) -> bool:
    """
    This function verfies the validity of a transaction given the current state of the blockchain and the transaction.
    It checks if the format of the transaction is correct, if the input transaction is valid, and if the signature is valid.
    If any of these checks fail, the function returns False.
    Otherwise, it returns True.

    :param blockchain: The current state of the blockchain (list of dict)
    :param transaction: The transaction to be verified (dict)
    :param mined: If the transaction has beened mined already (bool). By default False
    """

    # Check if the provided transaction has a valid type
    try:
        if transaction["type"] == 1:

            # Get the previous transaction id and index to check balance
            input_id = transaction["input"]["id"]
            input_index = transaction["input"]["n"]
            previousTransactions = None

            # Look for that transaction in the blockchain
            for block in blockchain:
                if input_id == block["id"]:
                    previousTransactions = block["tx"]["output"][input_index]
                    break

            # If not in the blockchain, return False
            if previousTransactions is None:
                return

            # Get the amount of coins in the input transaction
            previousAmount = int(previousTransactions["value"])

            # Check if the transaction has a change
            change = 0
            if previousAmount > int(transaction["output"][0]["value"]):

                # Get the change in the transaction
                # If there is no change when there should be, return False
                try:
                    change = int(transaction["output"][1]["value"])
                except IndexError:
                    return False

            # Check if the transaction amount is valid
            if previousAmount == int(transaction["output"][0]["value"]) + change:
                # Verify the signature of this transaction
                return verifySignature(transaction, previousTransactions["pub_key"], mined)
            else:
                return False
        else:
            return False
    except:
        return False


def calculateUserBalance(blockchain: dict, sk_key: SigningKey) -> tuple[dict, int]:
    """
    This function calculates the balance of a user given the blockchain and their secret key.
    It returns the wallet of the user (all transactions that they can use for future payments) and their balance.

    :param blockchain: The current state of the blockchain (list of dict)
    :param sk_key: The secret key of the user (ecdsa.SigningKey)

    :return: The wallet of the user (dict) and their balance (int)
    """

    # Get the pub key of the user
    pub_key = sk_key.get_verifying_key().to_string().hex()

    # Create an empty wallet for the user
    # Wallet is a dictionary of transactions that the user can use for future payments
    # Key is the id of the transaction and the index of the output
    # Value is the amount of coins in the transaction, the transaction itself, and the index of the output
    wallet = {}

    # Look through the blockchain to calculate the balance of the user
    for block in blockchain:

        # Account for varied size in the number of outputs
        try:
            # Check if its a payment by the user by checking signature
            if verifySignature(block["tx"], pub_key, True):

                # Get the input block id
                block_id = block["tx"]["input"]["id"]
                n = block["tx"]["input"]["n"]
                # Remove block from wallet if it used as input
                try:
                    del wallet[block_id + str(n)]

                except KeyError:
                    # Throw new blockchain error
                    raise Exception("Invalid blockchain")

            # Check if there are payments to the user

            # Check in slot 0
            if block["tx"]["output"][0]["pub_key"] == pub_key:
                amount = int(block["tx"]["output"][0]["value"])
                # Add the block to the wallet
                wallet[block["id"] + "0"] = {
                    "amount": amount,
                    "block": block,
                    "index": 0,
                }

            # Check in slot 1
            if block["tx"]["output"][1]["pub_key"] == pub_key:
                amount = int(block["tx"]["output"][1]["value"])
                # Add the block to the wallet
                wallet[block["id"] + "1"] = {
                    "amount": amount,
                    "block": block,
                    "index": 1,
                }

            # Check in slot 2
            if block["tx"]["output"][2]["pub_key"] == pub_key:
                amount = int(block["tx"]["output"][2]["value"])
                # Add the block to the wallet
                wallet[block["id"] + "2"] = {
                    "amount": amount,
                    "block": block,
                    "index": 2,
                }
        except IndexError:
            pass

            # Incoming payment elsewise?

    # NOTE DOes not count unverified transactions

    # Calculate the balance of the user
    balance = 0
    for block in wallet:
        balance += wallet[block]["amount"]

    # Return the wallet and balance of the user
    return wallet, balance


def createTransaction(
    wallet: dict, balance: int, sk: SigningKey, amount: int, to: str
) -> dict:
    """
    The following function creates a new tranaction object given the wallet of the user, their balance, their secret key, the amount of coins to be sent, and the public key of the recipient.
    It will throw an error if the user does not have enough funds to cover the transaction.

    :param wallet: The current state of the user's wallet (dict)
    :param balance: The current balance of the user (int)
    :param sk: The secret key of the user (ecdsa.SigningKey)
    :param amount: The amount of coins to be sent (int)
    :param to: The public key of the recipient (in hex string)

    :return: The transaction object (dict)
    """

    # Get the users public key
    pub_key = sk.get_verifying_key().to_string().hex()

    # Simple check if the user has enough funds
    if balance < amount:
        raise Exception("Insufficient funds")

    # Look in the wallet for a input block that can cover the FULL amount
    input_block = None
    for block in wallet:
        if wallet[block]["amount"] >= amount:
            input_block = wallet[block]
            break

    # If no block was found, throw an error
    if input_block is None:
        raise Exception("Merge input not supported")

    # Create the transaction
    transaction = {
        "type": 1,
        "input": {"id": input_block["block"]["id"], "n": input_block["index"]},
        "output": [{"pub_key": to, "value": amount}],
    }

    # Calculate the change
    if amount < input_block["amount"]:
        transaction["output"].append(
            {"pub_key": pub_key, "value": input_block["amount"] - amount}
        )

    # Sign the transaction
    transaction["sig"] = signTransaction(transaction, sk)

    # Remove block from wallet if it used as input
    try:
        del wallet[input_block["block"]["id"] + str(input_block["index"])]

    # Throw a error that the wallet is invalid (* Should not happen unless race condition *)
    except KeyError:
        # Throw new blockchain error
        raise Exception("Invalid wallet")

    # Return the transaction object
    return transaction


def verifyBlock(blockchain, block):
    """
    This function verfies a mined block adhears to the blockchain rules.
    It will check the following:
        - The format of the block is correct
        - Id of the block is calculated correctly
        - Tranaaction in the block is valid
        - The proof of work in the block is valid
        - And if the previous block is the last block added in the blockchain.

    If any of these checks fail, the function returns False.
    Otherwise, it returns True.

    :param blockchain: The current state of the blockchain (list of dict)
    :param block: The block to be verified (dict)

    :return: True if the block is valid, False otherwise

    """

    # Check if the block is of the correct type
    if block["type"] == 0:

        # Next check if prev is previous block is in the blockchain
        if block["prev"] == blockchain[-1]["id"]:

            # Check if the id of the block is valid
            block_id = hashlib.sha256(
                json.dumps(block["tx"], sort_keys=True).encode("utf8")
            ).hexdigest()
            if block_id == block["id"]:

                # Verfiy tranmsaction
                if verify(blockchain, block["tx"], True):

                    # Check if the proof of work is valid
                    blockHash = hashlib.sha256(
                        json.dumps(block["tx"], sort_keys=True).encode("utf8")
                        + block["prev"].encode("utf-8")
                        + block["nonce"].encode("utf-8")
                    ).hexdigest()
                    if int(blockHash, 16) < DIFFICULTY:
                        # If all checks pass, return True
                        return True
                    else:
                        print("Invalid proof of work")
                else:
                    print("Invalid transaction")
            else:
                print("Invalid block id")
        else:
            print("Invalid previous block")
    else:
        print("Invalid block format/type")

    # One or more checks failed, return False
    return False


def compareTransactions(transaction1: dict, transaction2: dict) -> bool:
    """
    This function compares if two transactions are the same.
    It will hash the input and output of the transactions and compare them.
    It helps detect double spending or if a tranaction is already in the blockchain/mined.

    :param transaction1: The first transaction to be compared (dict)
    :param transaction2: The second transaction to be compared (dict)

    :return: True if the transactions (inputs at a min) are the same, False otherwise
    """

    try:
        # Hash both the input and output of the transactions
        hash1 = hashlib.sha256(
            json.dumps(transaction1["input"], sort_keys=True).encode("utf8")
            + json.dumps(transaction1["output"], sort_keys=True).encode("utf8")
        ).hexdigest()
        hash2 = hashlib.sha256(
            json.dumps(transaction2["input"], sort_keys=True).encode("utf8")
            + json.dumps(transaction2["output"], sort_keys=True).encode("utf8")
        ).hexdigest()

        # Also hash only the inputs to check for double spending
        hash1_input = hashlib.sha256(
            json.dumps(transaction1["input"], sort_keys=True).encode("utf8")
        ).hexdigest()
        hash2_input = hashlib.sha256(
            json.dumps(transaction2["input"], sort_keys=True).encode("utf8")
        ).hexdigest()

        # Compare the hashes
        return hash1_input == hash2_input or hash1 == hash2
    except Exception as e:
        raise Exception("Invalid transaction")


def inBlockchain(blockchain: List[dict], transaction: dict) -> bool:
    """
    This function checks if a transaction already exists in the blockchain.
    If it already exists, means it has been mined or a client is attempting to double spend.
    If a transaction is in the blockchain, it will return True, otherwise False.

    :param blockchain: The current state of the blockchain (list of dict)
    :param transaction: The transaction to be checked (dict)

    :return: True if the transaction is in the blockchain, False otherwise

    """
    for block in blockchain:
        if compareTransactions(block["tx"], transaction):
            return True
    return False
