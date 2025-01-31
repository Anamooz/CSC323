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


def bit_recovery(output: str, mask: str, shift: int, left_shift=True) -> int:
    """
    This function recovers the input bits from the output bits and tthe mask and shift given to the tempering function
    IE: This function undoes a tempering function given the following format

        output = input ^ ((input <</>> shift) & mask)

    Args:
        output: The output bits of the tempering function given as a binary string
        mask: The mask used in the tempering function given as a binary string
        shift: The shift amount used in the tempering function
        left_shift: A boolean that determines if the shift is to the left or right
            If True then the shift is to the left
            Else the shift is to the right

    Returns:
        The input bits of the tempering function as an integer

    """

    # Creates a buffer to store the input bits
    input_bit_string = [0] * 32

    # For each bit in a 32 bit integer
    # Works from right to left
    for i in range(31, -1, -1):
        # Determine the bit at the current index
        input_bit_string[i] = bit_recovery_helper(output, mask, shift, i, left_shift)

    # Converts the binary string to an integer
    return int("".join(input_bit_string), 2)


def bit_recovery_helper(
    output: str, mask: str, shift: int, index: int, left_shift: bool
) -> str:
    """

    This function is a helper function for the bit_recovery function
    It detemines the value of the input bit at the current index

    Args:
        output: The output bits of the tempering function given as a binary string
        mask: The mask used in the tempering function given as a binary string
        shift: The shift amount used in the tempering function
        index: The current index of the bit being calculated
        left_shift: A boolean that determines if the shift is to the left or right
            If True then the shift is to the left
            Else the shift is to the right

    Returns:
        The value of the input bit at the current index as a binary string ( 0 | 1)

    """

    # Find the next shift to the left or right
    new_indwex = 0
    if left_shift:
        # Base cases
        if index >= (32 - shift):
            return output[index]
        new_indwex = index + shift
    else:
        # Base cases
        if index < shift:
            return output[index]
        new_indwex = index - shift

    # Recursive step
    # Check the output bir at the current index
    if output[index] == "1":
        # If one check if the mask bit is 1
        if mask[index] == "1":
            # Check if the shifted inpyut bit is also 1
            # x[i + shift] = x[i] ^ x[i + shift]
            # If it is then this bit must inside the and must be false
            # Otherwise the and returned true and 1
            return (
                "0"
                if bit_recovery_helper(output, mask, shift, new_indwex, left_shift)
                == "1"
                else "1"
            )
        else:
            # 1 must have came from input
            return "1"
    else:
        # If the output bit is 0
        # Then check the mask bit  was 1 see if the shifted input bit was 1
        # If shifted input is 1 then the index at the current bit must be 1
        # Otherwise the output bit must have been 0
        if mask[index] == "1":
            return (
                "1"
                if bit_recovery_helper(output, mask, shift, new_indwex, left_shift)
                == "1"
                else "0"
            )
        else:
            # If mask is 0 then the output bit must have been 0
            return "0"


def convertIntToBinaryString(number: int) -> str:
    """
    This function converts an integer to a binary string

    Args:
        number: The integer to convert to a binary string

    Returns:
        The binary string representation of the input integer
    """
    return format(number, "032b")


def untemper_number(number):
    print("-----------------")
    y = number
    print(y)
    y = bit_recovery(
        convertIntToBinaryString(y), convertIntToBinaryString(0xFFFFFFFF), l, False
    )
    print(y)
    y = bit_recovery(convertIntToBinaryString(y), convertIntToBinaryString(c), t)
    print(y)
    y = bit_recovery(convertIntToBinaryString(y), convertIntToBinaryString(b), s)
    print(y)
    return bit_recovery(
        convertIntToBinaryString(y), convertIntToBinaryString(d), u, False
    )


print(untemper_number(temper(12345)))
