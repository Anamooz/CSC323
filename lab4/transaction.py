from ecdsa import VerifyingKey, SigningKey
import json
from exampleTransaction import example_transaction, example_blockchain


def verifySignature(transaction, pubKey):
    try:
        # Remove coin base transaction
        # Coin base transactions are not signed and are located at index 2
        transaction["output"] = transaction["output"][:2]

        # Extract the signature and the message from the transaction
        signature = bytes.fromhex(transaction["sig"])

        message = json.dumps(transaction["input"], sort_keys=True).encode(
            "utf8"
        ) + json.dumps(transaction["output"], sort_keys=True).encode("utf8")

        # Create Verify Key
        vk = VerifyingKey.from_string(bytes.fromhex(pubKey))
        # Verify the signature
        return vk.verify(signature, message)
    except:
        return False


def signTransaction(transaction, privKey):

    # Remove any coin base transaction
    # Coin base transactions are not signed and are located at index 2
    transaction["output"] = transaction["output"][:2]

    # Extract the message from the transaction
    message = json.dumps(transaction["input"], sort_keys=True).encode(
        "utf8"
    ) + json.dumps(transaction["output"], sort_keys=True).encode("utf8")

    # Sign the message
    signature = privKey.sign(message)
    return signature.hex()


def verify(blockchain, transaction):
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
            return verifySignature(transaction, previousTransactions["pub_key"])
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
            if verifySignature(block["tx"], pub_key):
                # Get the input block id
                block_id = block["tx"]["input"]["id"]
                # Remove block from wallet if it used as input
                try:
                    del wallet[block_id]
                except KeyError:
                    # Throw new blockchain error
                    raise Exception("Invalid blockchain")
            # Incoming payment elsewise?
            elif block["tx"]["output"][0]["pub_key"] == pub_key:
                amount = block["tx"]["output"][0]["value"]
                # Add the block to the wallet
                wallet[block["id"]] = {"amount": amount, "block": block, "index": 0}
            elif block["tx"]["output"][1]["pub_key"] == pub_key:
                amount = block["tx"]["output"][1]["value"]
                # Add the block to the wallet
                wallet[block["id"]] = {"amount": amount, "block": block, "index": 1}
        except IndexError:
            pass

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

    return transaction


secret_key = SigningKey.from_string(bytes.fromhex("<input here>"))
user_wallet, user_balance = calculateUserBalance(example_blockchain, secret_key)
transaction = createTransaction(user_wallet, user_balance, secret_key, 10, "123456")
print(transaction)
