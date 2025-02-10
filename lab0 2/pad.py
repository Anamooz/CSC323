BLOCK_SIZE = 16


def pad(msg: bytes) -> bytes:
    padding_required = (
        BLOCK_SIZE
        if (len(msg) % BLOCK_SIZE == 0)
        else (BLOCK_SIZE - len(msg) % BLOCK_SIZE)
    )
    return msg + ((chr(padding_required).encode()) * padding_required)


def unpad(bytes: bytes) -> bytes:
    padding_required_to_remove = bytes[len(bytes) - 1]
    unpadded = bytes[: len(bytes) - padding_required_to_remove]
    if bytes[len(unpadded) :] == (
        chr(padding_required_to_remove).encode() * padding_required_to_remove
    ):
        return unpadded
    else:
        raise ValueError("Invalid padding")


print(unpad(pad(b"Yellow")))
