w, n, m, r = 32, 624, 397, 31
a = 0x9908B0DF
u, d = 11, 0xFFFFFFFF
s, b = 7, 0x9D2C5680
t, c = 15, 0xEFC60000
l = 18
f = 1812433253
lower_mask = (1 << r) - 1  # All 31 lower bits are set
upper_mask = 1 << r  # Only the 32nd bit is set
maxUInt32 = 2**32 - 1  # Max value for a 32 bit unsigned integer 0xFFFFFFFF


def temper(number):
    y = number
    y ^= (y >> u) & d
    y ^= (y << s) & b
    y ^= (y << t) & c
    y ^= y >> l
    return y


def untemper(z):
    """Reverse the tempering function of MT19937 to recover the original state value from output z."""

    # Step 1: Reverse y = y ^ (y >> 18)  (right shift, MSB to LSB)
    y = z
    y ^= y >> 18

    # Step 2: Reverse y = y ^ ((y << 15) & 0xEFC60000) (left shift, LSB to MSB)
    y ^= (y << 15) & 0xEFC60000

    # Step 3: Reverse y = y ^ ((y << 7) & 0x9D2C5680) (left shift, LSB to MSB)
    for i in range(0, 32, 7):
        y ^= (y << 7) & 0x9D2C5680

    # Step 4: Reverse y = x ^ ((x >> 11) & 0xFFFFFFFF) (right shift, MSB to LSB)
    x = y
    for i in range(4):  # Since bits propagate, repeat a few times for full recovery
        x ^= (x >> 11) & 0xFFFFFFFF
    return x


print(temper(5))
print(untemper(temper(5)))
