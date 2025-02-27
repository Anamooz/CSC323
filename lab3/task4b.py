"""
Name : Brian Kwong and Trycia Vong
"""

import requests
import time
import string
from scipy.stats import ttest_1samp
from statistics import median

BASE_URL = "http://localhost:5000/?q=foo&mac="
MAC_LENGTH = 20  # HMAC-SHA1 produces a 20-byte MAC (40 hex characters)
HEX_DIGITS = string.hexdigits[:16]  # 0-9, a-f # COllect all possuble hex characters
NUM_REQUESTS = 5


def findAnamoly(values):
    lowest_p_val = 1
    best_index = None
    for i in range(len(values)):
        # Remove that i value from the list
        new_values = values[:i] + values[i + 1 :]
        # Perform the t-test
        t_stat, p_val = ttest_1samp(new_values, values[i])
        # If the p-value is less than alpha, return the index
        if p_val < lowest_p_val:
            best_index = i
            lowest_p_val = p_val
        if p_val < 0.05:
            exit(1)
    return best_index


def time_request(mac_guess):
    """Send a request with the given MAC guess and return the response time."""
    url = f"{BASE_URL}{mac_guess}"
    start_time = time.perf_counter()
    requests.get(url)
    end_time = time.perf_counter()
    return end_time - start_time


def get_avg_response_time(mac_guess):
    """Take multiple measurements and return the median to reduce noise."""
    times = [time_request(mac_guess) for _ in range(NUM_REQUESTS)]
    return median(times)  # Use median to filter out network noise


def find_valid_mac():
    """Brute-force the MAC byte-by-byte using the timing leak."""
    guessed_mac = ""  # Start with an empty MAC

    # For each byte of the mac
    for i in range(MAC_LENGTH):
        timings = []  # Create a list to store the timings for each candidate

        # For each possible byte value
        # There are two hex characters per byte
        # Try all 256 possible values
        for candidate1 in HEX_DIGITS:
            for candidate2 in HEX_DIGITS:
                mac_try = (
                    guessed_mac
                    + candidate1
                    + candidate2
                    + "0" * ((MAC_LENGTH * 2) - len(guessed_mac) - 2)
                )
                # Collect the timings for each candidate
                duration = get_avg_response_time(mac_try)
                timings.append((candidate1 + candidate2, duration))

        # Sort candidates by longest response time
        timings_time = timings.copy()
        timings = [x[1] for x in timings]
        anamoly = findAnamoly(timings)
        best_guess = timings_time[anamoly][0]
        guessed_mac += best_guess
        print(f"Progress: {guessed_mac}")

    return guessed_mac


if __name__ == "__main__":
    valid_mac = find_valid_mac()
    print(f"Recovered MAC: {valid_mac}")
