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
    print(y)
    y ^= (y >> u) & d
    print(y)
    y ^= (y << s) & b
    print(y)
    y ^= (y << t) & c
    print(y)
    y ^= y >> l
    print(y)
    return y


def reverseStepFour(output: int, shift: int):
    return output ^ (output >> shift)


def reverseStep3And2(output: int, shift: int, mask: int):
    lower_bits = (0xFFFFFFFF >> (32 - shift)) & output
    lower_bits = (lower_bits << shift) & mask
    return output ^ lower_bits


def reverseStepOne(output: int, shift: int, mask: int):
    upper_bits = (0xFFFFFFFF << (32 - shift)) & output
    upper_bits = (upper_bits >> shift) & mask
    return output ^ upper_bits


def untemper(number):
    print("-----------------")
    y = number
    print(y)
    y = reverseStepFour(y, l)
    print(y)
    y = reverseStep3And2(y, t, c)
    print(y)
    y = reverseStep3And2(y, s, b)
    print(y)
    y = reverseStepOne(y, u, d)
    print(y)


# print(temper(5))
print(untemper(temper(5)))
