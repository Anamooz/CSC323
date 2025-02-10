import unittest
import unittest.util

"""
Name : Brian Kwong and Trycia Vong
"""


class MT19937:

    def __init__(self, seed):
        """

        This function defines all variables and constants used in the MT19937 algorithm.
        Args:
            seed (int): Seed used for the PRG generator. [0, 2**32 - 1] No negative numbers.
        """

        seed = int.from_bytes(seed, "little")  # Convert the seed to an integer

        # Checks if the seed is in the correct range
        if seed < 0 or seed >= 2**32:
            raise ValueError("Seed must be in the range [0, 2**32 - 1]")

        # Constants for MT19937
        # Obtained from Wikipedia article on Mersenne Twister

        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908B0DF
        self.u, self.d = 11, 0xFFFFFFFF
        self.s, self.b = 7, 0x9D2C5680
        self.t, self.c = 15, 0xEFC60000
        self.l = 18
        self.f = 1812433253
        self.lower_mask = (1 << self.r) - 1  # All 31 lower bits are set
        self.upper_mask = 1 << self.r  # Only the 32nd bit is set
        self.maxUInt32 = 2**32 - 1  # Max value for a 32 bit unsigned integer 0xFFFFFFFF

        # Initialize state array

        # Creates an array of size N for the buffer used in MT19937
        # Zeros out the array
        self.mt = [0] * self.n

        # Intalize the buffer with a list of numbers based off the seed
        self.initialize_mt_generator(seed)

    def initialize_mt_generator(self, seed):
        """

        The following function initalizes the MT19937 generator from a seed.

        Args:
           seed (int): Seed used for the PRG generator. [0, 2**32 - 1] No negative numbers.


        """
        self.mt[0] = seed  # Sets the seed as the first element in the buffer

        # For each of the remaining elements in the buffer calculate that number using the following formula :

        # x[i] = f * ((Xi-1) XOR ((Xi-1 >> 30 )) + i

        for i in range(1, self.n):
            self.mt[i] = (
                self.f * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2))) + i
            ) & self.maxUInt32  # Ensures we only use lower 32 bits Mimics the C code
        self.index = (
            self.n
        )  # Note this inital buffer is not used directly to generate numbers

    def twist(self):
        """

        Generate the next set of n values in the buffer once the previous set of numbers have been exhausted.

        ((Xk + n ) where k > 0
                    ((Xk + n) =  ((Xk + m) (CONCAT(upperBits((Xk),lowerBits((Xk + 1) )A)
        Which translates to the following steps:
            1. x[i] = (x[i] & upper_mask) + (x[i + 1] & lower_mask)
            2. If x[i] is odd then xA = x[i] >> 1 XOR a else just xA = x[i] >> 1) # Applies the matrix A transformation
            3. x[i] = x[k + m] XOR xA

        """

        for i in range(self.n):

            first_element = self.mt[i]
            second_element = self.mt[
                (i + 1) % self.n
            ]  # Checks if the element if over the size of the size of the buffer
            # If so wrap around to the beginning of the buffer

            x = (first_element & self.upper_mask) + (second_element & self.lower_mask)

            # Apply the matrix A transformation to the value of x using the following formula :
            # If x[i] is odd then xA = x[i] >> 1 XOR a else just xA = x[i] >> 1)
            # Even is defined as the last bit not being set

            xA = x >> 1
            if x % 2:  # lowest bit of x is 1
                xA ^= self.a

            offset_element = self.mt[(i + self.m) % self.n]
            # XOR xA with X[k+m] element to get the final twisted value
            self.mt[i] = offset_element ^ xA
        self.index = 0  # Reset the index back to 0

    def extract_number(self):
        """

        The following function that pops a number off the buffer and applies the tempering function to it.

        The tempering function is defined as follows:
            1. y = x XOR ((x >> u) AND d)
            2. y = y XOR ((y << s) AND b)
            3. y = y XOR ((y << t) AND c)
            4. y = y XOR (y >> 1)

        The tempered value is then returned.

        """

        # If the buffer has been exhausted generate a new set of numbers before popping the next number
        if self.index >= self.n:
            print("Twisting")
            self.twist()

        # Pop the next number from the buffer
        y = self.mt[self.index]
        # Slide the index to the next number for the next round of generation
        self.index += 1
        # Applies the tempering function
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        return y  # Returns the tempered value
