"""
Name : Brian Kwong and Trycia Vong
"""

import requests
import time
import string

BASE_URL = "http://localhost:8080/?q=foo&mac="
MAC_LENGTH = 20  # HMAC-SHA1 produces a 20-byte MAC (40 hex characters)
HEX_DIGITS = string.hexdigits[:16]  # 0-9, a-f # COllect all possuble hex characters


def time_request(mac_guess):
    """Send a request with the given MAC guess and return the response time."""
    url = f"{BASE_URL}{mac_guess}"
    start_time = time.perf_counter()
    requests.get(url)
    end_time = time.perf_counter()
    return end_time - start_time


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
                duration = time_request(mac_try)
                timings.append((candidate1 + candidate2, duration))

        # Sort candidates by longest response time
        best_guess = max(timings, key=lambda x: x[1])[0]
        guessed_mac += best_guess
        print(f"Progress: {guessed_mac}")

    return guessed_mac


if __name__ == "__main__":
    valid_mac = find_valid_mac()
    print(f"Recovered MAC: {valid_mac}")
