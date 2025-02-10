import time
from random import randint
from task1 import MT19937
from tools import *

global seed


def orcale():
    time.sleep(randint(5, 60))
    global seed
    seed = int(time.time())
    x = MT19937(seed).generate_number()
    time.sleep(randint(5, 60))
    return x


def seedCracker(input_function: callable):

    # Get the seed
    seed2 = int(time.time())
    # Get the output
    output = input_function()
    # Loop through the possible seeds
    for i in range(5, 60):
        # Create a new MT19937 with the seed
        mt = MT19937(seed2 + i)
        # Check if the output is the same
        if mt.generate_number() == output:
            print(f"Seed: {seed2 + i}")
            print(f"Seed matched: {(seed2 + i) == seed}")
            break

if __name__ == "__main__":
    seedCracker(orcale)
