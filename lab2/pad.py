"""
Name : Brian Kwong and Trycia Vong
"""

BLOCK_SIZE = 16


def pad(msg: bytes) -> bytes:
    padding_required = (
        BLOCK_SIZE
        if (len(msg) % BLOCK_SIZE == 0)
        else (BLOCK_SIZE - len(msg) % BLOCK_SIZE)
    )
    return msg + ((padding_required.to_bytes(1)) * padding_required)


def unpad(text: bytes) -> bytes:
    print(len(text))
    if len(text) <= 0 or len(text) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padding")
    padding_required_to_remove = text[len(text) - 1]
    unpadded = text[: len(text) - padding_required_to_remove]
    if text[len(unpadded) :] == (
        padding_required_to_remove.to_bytes(1) * padding_required_to_remove
    ):
        return unpadded
    else:
        raise ValueError("Invalid padding")


print(unpad(pad(b"Yellow")))
