# Used to compare our implementation of SHA-1 with the one from the Crypto library.
from Crypto.Hash import SHA1


def leftrotate(n, b):
    # Leff shift n by b bits
    # OR w/ right shift n by 32 - b bits
    # AND w/ 0xFFFFFFFF to get 32-bit

    # In short shift n by b bits to the left and extract the lower 32 bits
    # Assume bits wrap around

    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF


def sha1Helper(message, i, h0, h1, h2, h3, h4):
    chunk = message[i : i + 64]
    # Create 80 byte buffer for SHA-1
    w = [0] * 80

    # break chunk into sixteen 32-bit big-endian words w[i], 0 ≤ i ≤ 15
    # Get 4 bytes (32 bits) and convert it to big-endian
    # The first 16 bytes of the buffer are the original message
    for j in range(16):
        w[j] = int.from_bytes(chunk[j * 4 : j * 4 + 4], "big")

    # Message schedule: extend the sixteen 32-bit words into eighty 32-bit words
    # AAppl
    for j in range(16, 80):
        # Create a 32-bit word
        # N = (N-3 XOR N-8 XOR N-14 XOR N-16)
        # Left shift N by 1
        w[j] = leftrotate((w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16]), 1)

    # Initialize hash value for this chunk:
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4

    # Main hashing function loop:
    # For each value
    for j in range(80):
        # First 20 values
        if 0 <= j <= 19:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        # Next 20 values
        elif 20 <= j <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        # Next 20 values
        elif 40 <= j <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        # Last 20 values
        elif 60 <= j <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        # Calculate the temp value for that index
        temp = (leftrotate(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
        e = d
        d = c
        c = leftrotate(b, 30)
        b = a
        a = temp

    # Add this chunk's hash to result so far:
    # Convert the hash to 32-bit
    h0 = (h0 + a) & 0xFFFFFFFF
    h1 = (h1 + b) & 0xFFFFFFFF
    h2 = (h2 + c) & 0xFFFFFFFF
    h3 = (h3 + d) & 0xFFFFFFFF
    h4 = (h4 + e) & 0xFFFFFFFF
    return h0, h1, h2, h3, h4


def sha1(message):

    # Initialize variables:

    # h0 = 0x67452301
    # h1 = 0xEFCDAB89
    # h2 = 0x98BADCFE
    # h3 = 0x10325476
    # h4 = 0xC3D2E1F0
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing:
    # The message length in bits (always a multiple of the number of bits in a character).
    original_byte_len = len(message)

    # Get the number bits in the message
    original_bit_len = original_byte_len * 8

    # Add 1 to the end of the message
    message += b"\x80"

    # Pad the msg to 56 bytes (448
    # Last 8 bytes will be used to store the length of the original message)
    new_msg_len = (original_byte_len + 1) % 64
    message += b"\x00" * ((56 - new_msg_len) % 64)

    # Append the original message length in bits as a 64-bit big-endian integer
    message += int.to_bytes(original_bit_len, 8, "big")

    # Process the message in successive 512-bit chunks:
    for i in range(0, len(message), 64):
        h0, h1, h2, h3, h4 = sha1Helper(message, i, h0, h1, h2, h3, h4)

    # Produce the final hash value (big-endian) as a 160-bit number:
    # The final hash is a concatenation of the 5 32-bit hash values
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return hh


# Create unittest to ensure the hash value is correct
import unittest


class sha1_test(unittest.TestCase):

    def test_sha1(self):
        message = b"abc"
        hash_value = sha1(message)
        real_hash = SHA1.new(message).hexdigest()
        self.assertEqual(hash_value, int(real_hash, 16))

    def test_sha2(self):
        message = b"Lucky merge on the gems,keys and greenhouses Testing on a message that is longer than 512 bits"
        hash_value = sha1(message)
        real_hash = SHA1.new(message).hexdigest()
        self.assertEqual(hash_value, int(real_hash, 16))

    def two_different_msg_test(self):
        message1 = b"What the sigma"
        message2 = b"What the sigma?"
        hash_value1 = sha1(message1)
        hash_value2 = sha1(message2)
        self.assertNotEqual(hash_value1, hash_value2)


if __name__ == "__main__":
    unittest.main()
