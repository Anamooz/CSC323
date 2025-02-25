import requests
import time
import string

BASE_URL = "http://localhost/?q=foo&mac="
MAC_LENGTH = 20  # HMAC-SHA1 produces a 20-byte MAC
HEX_DIGITS = string.hexdigits[:16]  # 0-9, a-f


def time_request(mac_guess):
    """Send a request with the given MAC guess and return the response time."""
    url = f"{BASE_URL}{mac_guess}"
    start_time = time.perf_counter()
    response = requests.get(url)
    end_time = time.perf_counter()
    return end_time - start_time, response.text


def find_valid_mac():
    """Brute-force the MAC byte-by-byte using the timing leak."""
    guessed_mac = ""  # Start with an empty MAC

    for i in range(MAC_LENGTH):
        timings = []

        for candidate in HEX_DIGITS:
            mac_try = (
                guessed_mac
                + candidate
                + "0" * (2 * (MAC_LENGTH - len(guessed_mac) - 1))
            )  # Pad remaining with zeros
            duration, _ = time_request(mac_try)
            timings.append((candidate, duration))

        # Sort candidates by longest response time
        best_guess = max(timings, key=lambda x: x[1])[0]
        guessed_mac += best_guess
        print(f"Progress: {guessed_mac}")

    return guessed_mac


if __name__ == "__main__":
    valid_mac = find_valid_mac()
    print(f"Recovered MAC: {valid_mac}")
