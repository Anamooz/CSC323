class MT19937:
    def __init__(self, seed):
        # Constants for MT19937

        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908B0DF
        self.u, self.d = 11, 0xFFFFFFFF
        self.s, self.b = 7, 0x9D2C5680
        self.t, self.c = 15, 0xEFC60000
        self.l = 18
        self.f = 1812433253

        # Initialize state array
        self.mt = [
            0
        ] * self.n  # Creates an array of size N for the buffer used in MT19937
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = ~self.lower_mask & ((1 << self.w) - 1)

        self.seed_mt(seed)

    def seed_mt(self, seed):
        """

        The following function initalizes the MT19937 generator from a seed.

        Args:
            seed (int): Seed used for the PRG generator.


        """
        self.mt[0] = seed  # Sets the seed as the first element in the buffer
        for i in range(1, self.n):
            self.mt[i] = (
                self.f * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2))) + i
            ) & 0xFFFFFFFF
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

        # Tempering
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        return y & 0xFFFFFFFF


# Example usage and verification
if __name__ == "__main__":
    seed = 12345
    mt = MT19937(seed)

    # Generate the first 10 numbers
    results = [mt.extract_number() for _ in range(10)]
    print("First 10 outputs:", results)

    # Verify deterministic behavior
    mt2 = MT19937(seed)
    results2 = [mt2.extract_number() for _ in range(10)]
    print("Verification:", results == results2)
