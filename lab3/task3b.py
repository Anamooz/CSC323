# function hmac is
#     input:
#         key:        Bytes    // Array of bytes
#         message:    Bytes    // Array of bytes to be hashed
#         hash:       Function // The hash function to use (e.g. SHA-1)
#         blockSize:  Integer  // The block size of the hash function (e.g. 64 bytes for SHA-1)
#         outputSize: Integer  // The output size of the hash function (e.g. 20 bytes for SHA-1)

#     // Compute the block sized key
#     block_sized_key = computeBlockSizedKey(key, hash, blockSize)

#     o_key_pad ← block_sized_key xor [0x5c blockSize]   // Outer padded key
#     i_key_pad ← block_sized_key xor [0x36 blockSize]   // Inner padded key

#     return  hash(o_key_pad ∥ hash(i_key_pad ∥ message))


def HMAC(key: bytes, message: bytes, hashFunction, blockSize: int, outputSize: int):
    block_sized_key = computeBlockSizeKey(key, hashFunction, blockSize)
    o_key_pad = bytes([x ^ 0x5C for x in block_sized_key])
    i_key_pad = bytes([x ^ 0x36 for x in block_sized_key])
    return hashFunction(o_key_pad + hashFunction(i_key_pad + message))


# function computeBlockSizedKey is
#     input:
#         key:        Bytes    // Array of bytes
#         hash:       Function // The hash function to use (e.g. SHA-1)
#         blockSize:  Integer  // The block size of the hash function (e.g. 64 bytes for SHA-1)

#     // Keys longer than blockSize are shortened by hashing them
#     if (length(key) > blockSize) then
#         key = hash(key)

#     // Keys shorter than blockSize are padded to blockSize by padding with zeros on the right
#     if (length(key) < blockSize) then
#         return  Pad(key, blockSize) // Pad key with zeros to make it blockSize bytes long

#     return  key


def computeBlockSizeKey(key: bytes, hashFunction, blockSize: int):
    if len(key) > blockSize:
        key = hashFunction(key)
    if len(key) < blockSize:
        return key + b"\x00" * (blockSize - len(key))
    return key


# Create unittest to ensure the hash value is correct
import unittest
from task2a import sha1Digest as sha1


class sha1_test(unittest.TestCase):

    # test_case = 1
    # key = 0x0B0B0B0B0B0B0B0B0B0B0B0B0B0B0B0B0B0B0B0B
    # key_len = 20
    # data = "Hi There"
    # data_len = 8
    # digest = 0xB617318655057264E28BC0B6FB378C8EF146BE00

    def test_HMAC1(self):
        key = bytes.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")
        data = b"Hi There"
        hash_value = int.from_bytes(HMAC(key, data, sha1, 64, 20), "big")
        digest = 0xB617318655057264E28BC0B6FB378C8EF146BE00
        self.assertEqual(hash_value, digest)

    # test_case =     2
    # key =           "Jefe"
    # key_len =       4
    # data =          "what do ya want for nothing?"
    # data_len =      28
    # digest =        0xeffcdf6ae5eb2fa2d27416d5f184df9c259a7c79

    def test_HMAC2(self):
        key = b"Jefe"
        data = b"what do ya want for nothing?"
        hash_value = int.from_bytes(HMAC(key, data, sha1, 64, 20), "big")
        digest = 0xEFFCDF6AE5EB2FA2D27416D5F184DF9C259A7C79
        self.assertEqual(hash_value, digest)

    # test_case =     3
    # key =           0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    # key_len =       20
    # data =          0xdd repeated 50 times
    # data_len =      50
    # digest =        0x125d7342b9ac11cd91a39af48aa17b4f63f175d3

    def test_HMAC3(self):
        key = bytes.fromhex("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        data = bytes.fromhex("dd" * 50)
        hash_value = int.from_bytes(HMAC(key, data, sha1, 64, 20), "big")
        digest = 0x125D7342B9AC11CD91A39AF48AA17B4F63F175D3
        self.assertEqual(hash_value, digest)


if __name__ == "__main__":
    unittest.main()
