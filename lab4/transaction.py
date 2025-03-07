from ecdsa import VerifyingKey, SigningKey
import json
from exampleTransaction import example_transaction


def verifySignature(transaction, pubKey):

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


# Example transaction
transaction = example_transaction
sk = SigningKey.from_string(
    bytes.fromhex("704091922fea99ba984f1b9ac5b8387b2f430f2617a8c289")
)
vk = sk.get_verifying_key()
pubKey = vk.to_string().hex()
print("Public Key: ", pubKey)
sig = signTransaction(transaction, sk)
print("Signature: ", transaction["sig"])
transaction["sig"] = sig
#print(verifySignature(transaction, pubKey))


# def verify(blockchain, transaction):
#     # Check if the tranaction?
#     if transaction["type"] == 1:

#         # Get the previous transaction id and index to check balance
#         input_id = transaction["input"]["id"]
#         input_index = transactions["input"]["n"]
#         previousTransactions = None
#         # Look for that transaction in the blockchain
#         for block in blockchain:
#             transactions = block["tx"]
#             if input_id == transactions["input"]["id"]:
#                 previousTransactions = transactions
#                 break

#         # If not in the blockchain, return False
#         if previousTransactions is None:
#             return

#         # Get the amount of coins in the input transaction
#         previousAmount = previousTransactions["output"][input_index]["value"]

#         # Check if the transaction amount is valid
#         if previousAmount >= transaction["output"][0]["value"]:
#             # Verify the signature of this transaction
#             return verifySignature(transaction, previousTransactions["output"][input_index]["pubKey"]):
#         else:
#             return False
#     else:
#         return False
