import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

FACEBOOK_EMAIL = os.getenv("FACEBOOK_EMAIL")
FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")
FACEBOOK_BASE_URL = "https://www.facebook.com/"

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
chrome_options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=chrome_options)
driver.get(FACEBOOK_BASE_URL)

COOKIE_TERM_CSS_SELECTOR = "._42ft._4jy0._al65._4jy3._4jy1.selected._51sy"
INPUT_TEXT_CSS_SELECTOR = "//input[@type='text']"
PASSWORD_CSS_SELECTOR = "//input[@placeholder='Hasło']"
SUBMIT_BUTTON_SELECTOR = "//button[@type='submit']"
wait = WebDriverWait(driver, 10)

def close_cookie_term(cookie_css_selector: str) -> None:
    button = driver.find_element(By.CSS_SELECTOR, cookie_css_selector)
    button.click()


def facebook_login(username_selector: str, password_selector: str) -> None:
    user_name = wait.until(EC.presence_of_element_located((By.XPATH, username_selector)))
    password = driver.find_element(By.XPATH, password_selector)

    user_name.send_keys(FACEBOOK_EMAIL)
    password.send_keys(FACEBOOK_PASSWORD)

    log_in_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_SELECTOR)
    log_in_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']")))


def security_code(security_code_selector: str) -> None:
    security_code_input = driver.find_elements(By.XPATH, security_code_selector)
    if security_code_input:
        security_code = input("Enter your security code: ")
        security_code_input[0].send_keys(security_code)

    save_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_SELECTOR)
    save_button.click()


