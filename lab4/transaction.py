from ecdsa import VerifyingKey, SigningKey
import json
from exampleTransaction import example_transaction, example_blockchain
import hashlib
from mining import createBlock, hasGPU

DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def newTransaction(client, sk, to, amount):
    try:
        transaction = createTransaction(client.wallet, client.balance, sk, amount, to)
        client.send_to_nodes(transaction)
    except Exception as Errro:
        print("Failed to create transaction: ", Errro)


def verifySignature(transaction, pubKey, fromChain=False):
    try:

        # If from the blockchain, remove the coin base or last transaction
        coreTranaction = transaction["output"]
        if fromChain:
            coreTranaction = transaction["output"][:-1]

        # Extract the signature and the message from the transaction
        signature = bytes.fromhex(transaction["sig"])

        message = json.dumps(transaction["input"], sort_keys=True).encode(
            "utf8"
        ) + json.dumps(coreTranaction, sort_keys=True).encode("utf8")

        # Create Verify Key
        vk = VerifyingKey.from_string(bytes.fromhex(pubKey))
        # Verify the signature
        return vk.verify(signature, message)
    except Exception as e:
        return False


def signTransaction(transaction, privKey):

    # Extract the message from the transaction

    message = json.dumps(transaction["input"], sort_keys=True).encode(
        "utf8"
    ) + json.dumps(transaction["output"][:2], sort_keys=True).encode("utf8")

    # Sign the message
    signature = privKey.sign(message)
    return signature.hex()


def verify(blockchain, transaction, mined=False):
    # Check if the tranaction?
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
        previousAmount = previousTransactions["value"]
        change = 0
        try:
            change = transaction["output"][1]["value"]
        except IndexError:
            pass

        # Check if the transaction amount is valid
        if previousAmount == transaction["output"][0]["value"] + change:
            # Verify the signature of this transaction
            return verifySignature(transaction, previousTransactions["pub_key"], mined)
        else:
            return False
    else:
        return False


def calculateUserBalance(blockchain, sk_key):

    # Get the pub key of the user
    pub_key = sk_key.get_verifying_key().to_string().hex()

    # Look through the blockchain to calculate the balance of the user
    # Dict of block id unu
    wallet = {}
    for block in blockchain:
        # Check if its a payout of the user by checking signature

        try:
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
            # Incoming payment elsewise?
            if block["tx"]["output"][0]["pub_key"] == pub_key:
                amount = block["tx"]["output"][0]["value"]
                # Add the block to the wallet
                wallet[block["id"] + "0"] = {
                    "amount": amount,
                    "block": block,
                    "index": 0,
                }
            if block["tx"]["output"][1]["pub_key"] == pub_key:
                amount = block["tx"]["output"][1]["value"]
                # Add the block to the wallet
                wallet[block["id"] + "1"] = {
                    "amount": amount,
                    "block": block,
                    "index": 1,
                }
            if block["tx"]["output"][2]["pub_key"] == pub_key:
                amount = block["tx"]["output"][2]["value"]
                # Add the block to the wallet
                wallet[block["id"] + "2"] = {
                    "amount": amount,
                    "block": block,
                    "index": 2,
                }
        except IndexError:
            pass

            # Incoming payment elsewise?

    # Calculate the balance of the user
    balance = 0
    for block in wallet:
        balance += wallet[block]["amount"]

    return wallet, balance


def createTransaction(wallet, balance, sk, amount, to):
    # Get the users public key
    pub_key = sk.get_verifying_key().to_string().hex()

    # Simple check if the user has enough funds
    if balance < amount:
        raise Exception("Insufficient funds")

    # Look in the wallet for a input block that can cover the amount
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
    if amount < input_block["amount"]:
        transaction["output"].append(
            {"pub_key": pub_key, "value": input_block["amount"] - amount}
        )

    # Sign the transaction
    transaction["sig"] = signTransaction(transaction, sk)

    # Remove block from wallet if it used as input
    try:
        del wallet[input_block["block"]["id"] + str(input_block["index"])]
    except KeyError:
        # Throw new blockchain error
        raise Exception("Invalid blockchain")

    return transaction


def verifyBlock(blockchain, block):
    # Check if the block is a valid block

    # First check if the previous block is in the blockchain
    if block["prev"] == blockchain[-1]["id"]:

        # Check if the id of the block is valid
        block_id = hashlib.sha256(
            json.dumps(block["tx"], sort_keys=True).encode("utf8")
        ).hexdigest()
        if block_id == block["id"]:

            # Verfiy tranmsaction
            if verify(blockchain, block["tx"], True):
                # Check if the proof of work is valuid
                blockHash = hashlib.sha256(
                    json.dumps(block["tx"], sort_keys=True).encode("utf8")
                    + block["prev"].encode("utf-8")
                    + block["nonce"].encode("utf-8")
                ).hexdigest()
                if int(blockHash, 16) < DIFFICULTY:
                    return True

    return False


def compareTransactions(transaction1, transaction2):
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


def inBlockchain(blockchain, transaction):
    for block in blockchain:
        if compareTransactions(block["tx"], transaction):
            return True
    return False


# secret_key = SigningKey.from_string(bytes.fromhex("<input here>"))
# user_wallet, user_balance = calculateUserBalance(example_blockchain, secret_key)
# transaction = createTransaction(user_wallet, user_balance, secret_key, 10, "123456")
# print(transaction)

# new_block = createBlock(example_transaction, example_blockchain[-1]["id"], hasGPU)
# print(verifyBlock(example_blockchain, new_block))
