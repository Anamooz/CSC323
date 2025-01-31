def bit_recovery(output, mask, shift, left_shift=True):
    input_bit_string = [0] * 32
    for i in range(31, -1, -1):
        input_bit_string[i] = bit_recovery_helper(output, mask, shift, i, left_shift)
    return int("".join(input_bit_string), 2)


def bit_recovery_helper(output, mask, shift, index, left_shift):
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


print(bit_recovery(format(12351, "032b"), format(0xFFFFFFFF, "032b"), 11, False))
