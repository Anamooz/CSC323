# Import the require libraries
from selenium import webdriver
from selenium.webdriver.common.by import By

USERNAME = "example_usernam2e"
PASSWORD = "example_password"

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

# Waits for the user to press enter and close the browser
input("Press Enter to continue...")
