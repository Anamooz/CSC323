# Note 1: All variables are unsigned 32-bit quantities and wrap modulo 232 when calculating, except for
#         ml, the message length, which is a 64-bit quantity, and
#         hh, the message digest, which is a 160-bit quantity.
# Note 2: All constants in this pseudo code are in big endian.
#         Within each word, the most significant byte is stored in the leftmost byte position
from socket import ntohl

# Initialize variables:

# h0 = 0x67452301
# h1 = 0xEFCDAB89
# h2 = 0x98BADCFE
# h3 = 0x10325476
# h4 = 0xC3D2E1F0

h0 = ntohl(0x67452301)
h1 = ntohl(0xEFCDAB89)
h2 = ntohl(0x98BADCFE)
h3 = ntohl(0x10325476)
h4 = ntohl(0xC3D2E1F0)


# Pre-processing:
# append the bit '1' to the message e.g. by adding 0x80 if message length is a multiple of 8 bits.
# append 0 ≤ k < 512 bits '0', such that the resulting message length in bits
#    is congruent to −64 ≡ 448 (mod 512)
# append ml, the original message length in bits, as a 64-bit big-endian integer.
#    Thus, the total length is a multiple of 512 bits.

# Process the message in successive 512-bit chunks:
# break message into 512-bit chunks
# for each chunk
#     break chunk into sixteen 32-bit big-endian words w[i], 0 ≤ i ≤ 15

#     Message schedule: extend the sixteen 32-bit words into eighty 32-bit words:
#     for i from 16 to 79
#         Note 3: SHA-0 differs by not having this leftrotate.
#         w[i] = (w[i-3] xor w[i-8] xor w[i-14] xor w[i-16]) leftrotate 1

#     Initialize hash value for this chunk:
#     a = h0
#     b = h1
#     c = h2
#     d = h3
#     e = h4

#     Main loop:[3][56]
#     for i from 0 to 79
#         if 0 ≤ i ≤ 19 then
#             f = (b and c) or ((not b) and d)
#             k = 0x5A827999
#         else if 20 ≤ i ≤ 39
#             f = b xor c xor d
#             k = 0x6ED9EBA1
#         else if 40 ≤ i ≤ 59
#             f = (b and c) or (b and d) or (c and d)
#             k = 0x8F1BBCDC
#         else if 60 ≤ i ≤ 79
#             f = b xor c xor d
#             k = 0xCA62C1D6

#         temp = (a leftrotate 5) + f + e + k + w[i]
#         e = d
#         d = c
#         c = b leftrotate 30
#         b = a
#         a = temp

#     Add this chunk's hash to result so far:
#     h0 = h0 + a
#     h1 = h1 + b
#     h2 = h2 + c
#     h3 = h3 + d
#     h4 = h4 + e

# Produce the final hash value (big-endian) as a 160-bit number:
# hh = (h0 leftshift 128) or (h1 leftshift 96) or (h2 leftshift 64) or (h3 leftshift 32) or h4
import struct


def leftrotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF


def sha1(message):

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
        chunk = message[i : i + 64]
        # Create 80 byte buffer for SHA-1
        w = [0] * 80

        # break chunk into sixteen 32-bit big-endian words w[i], 0 ≤ i ≤ 15
        # Get 4 bytes (32 bits) and convert it to big-endian
        for j in range(16):
            w[j] = int.from_bytes(chunk[j * 4 : j * 4 + 4], "big")

        # Message schedule: extend the sixteen 32-bit words into eighty 32-bit words
        for j in range(16, 80):
            w[j] = leftrotate((w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16]), 1)

        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # Main loop:
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= j <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (leftrotate(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            e = d
            d = c
            c = leftrotate(b, 30)
            b = a
            a = temp

        # Add this chunk's hash to result so far:
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Produce the final hash value (big-endian) as a 160-bit number:
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return hh


# Example usage:
message = b"abc"
hash_value = sha1(message)
print(f"SHA-1 hash of '{message.decode()}' is: {hash_value:040x}")
