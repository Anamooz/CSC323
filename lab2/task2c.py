import requests
from tools import *
from selenium import webdriver


# Set the URL for the session

# Make 10000 random accounts
URL = "http://localhost:8080/register"

# # make the attack account
session = requests.Session()
username = ("x" * 11) + "admin" + (chr(0) * 10) + chr(11) + ("x" * 4)
payload = {"user": username, "password": "password123", "register": ""}
response = session.post(URL, data=payload)


# user=xxxxxx...|admin....|xxxx&uid=1&role=user.....
# user=xxxxxx...admin....&uid=1&role=admin....
LOGIN_URL = "http://localhost:8080/"
payload = {"user": username, "password": "password123", "Login": ""}
response = session.post(LOGIN_URL, data=payload)


cookie = session.cookies.get_dict()["auth_token"]
cookie = hex_to_ascii(cookie)

adminCookie = cookie[16:32]
newAdminCookie = cookie[:-16] + adminCookie
newAdminCookie = ascii_to_hex(newAdminCookie)
session.cookies.set("auth_token", newAdminCookie)

HOME_URL = "http://localhost:8080/home"
response = session.get(HOME_URL)
with open("output.html", "w") as f:
    f.write(response.text)
driver = webdriver.Edge()
driver.get(LOGIN_URL)
driver.add_cookie({"name": "auth_token", "value": newAdminCookie})
driver.get(HOME_URL)
input("Press Enter to continue...")
