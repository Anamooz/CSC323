import unittest
import unittest.util


class MT19937:

    def __init__(self, seed):
        """

        This function defines all variables and constants used in the MT19937 algorithm.
        Args:
            seed (int): Seed used for the PRG generator. [0, 2**32 - 1] No negative numbers.
        """

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

        # Initialize state array

        # Creates an array of size N for the buffer used in MT19937
        # Zeros out the array
        self.mt = [0] * self.n

        # Intalize the buffer with a list of numbers based off the seed
        self.seed_mt(seed)

    def seed_mt(self, seed):
        """

        The following function initalizes the MT19937 generator from a seed.

        Args:
           seed (int): Seed used for the PRG generator. [0, 2**32 - 1] No negative numbers.


        """
        self.mt[0] = seed  # Sets the seed as the first element in the buffer
        for i in range(1, self.n):
            self.mt[i] = (
                self.f * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2))) + i
            )
        self.index = self.n

    def twist(self):
        """Generate the next n values from the series x."""
        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) + (
                self.mt[(i + 1) % self.n] & self.lower_mask
            )
            xA = x >> 1
            if x % 2 != 0:  # lowest bit of x is 1
                xA ^= self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0

    def extract_number(self):
        """Extract a tempered value based on mt[index]."""
        if self.index >= self.n:
            if self.index > self.n:
                raise Exception("Generator was never seeded")
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        # Applies the tempering function
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        return y & 0xFFFFFFFF


# Example usage and verification
class Test_MT19937(unittest.TestCase):

    def test_deterministic_output(self):
        """
        Two instances of MT19937 with the same seed should produce the same sequence of numbers.
        This makes the algorithm deterministic.
        """

        seed = 88888
        mt = MT19937(seed)
        # Generate the first 10 numbers
        results = [mt.extract_number() for _ in range(10)]

        mt2 = MT19937(seed)
        results2 = [mt2.extract_number() for _ in range(10)]

        self.assertEqual(results, results2)

    def test_randomness(self):
        """
        Different seed should produce different random numbers

        """

        seed = 88888
        mt = MT19937(seed)
        # Generate the first 10 numbers
        results = [mt.extract_number() for _ in range(10)]

        # Generate the first 10 numbers with a different seed
        mt2 = MT19937(seed + 1)
        results2 = [mt2.extract_number() for _ in range(10)]

        self.assertNotEqual(results, results2)

    def test_distinct_randomness(self):
        """
        Different seed should produce different random numbers
        Each number produced from the first 10 numbers should be distinct

        """

        seed = 88888
        mt = MT19937(seed)
        # Generate the first 10 numbers
        results = set([mt.extract_number() for _ in range(10)])

        # Generate the first 10 numbers with a different seed
        mt2 = MT19937(seed + 1)
        results2 = set([mt2.extract_number() for _ in range(10)])

        # There shoiuld be no intersection between the two sets of numbers generated
        self.assertEqual(len(results.intersection(results2)), 0)

    def invalid_seeds(self):
        """

        Tests if invalid seeds are handled correctly and raises a ValueError

        """

        with self.assertRaisesRegex(ValueError, "Seed must be in the range"):
            MT19937(-1)
        with self.assertRaisesRegex(ValueError, "Seed must be in the range"):
            MT19937(2**32)


if __name__ == "__main__":
    unittest.main()
    seed = 88888
    mt = MT19937(seed)
    # Generate the first 10 numbers
    results = set([mt.extract_number() for _ in range(10)])
