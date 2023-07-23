import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


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


class FacebookLogIn:
    def __init__(self, driver: webdriver.Chrome = driver) -> None:
        self.email = os.getenv("FACEBOOK_EMAIL")
        self.password = os.getenv("FACEBOOK_PASSWORD")
        self.base_url = "https://www.facebook.com/"
        self.driver = driver
        self.driver.get(self.base_url)
        self.cookie_term_css_selector = "._42ft._4jy0._al65._4jy3._4jy1.selected._51sy"
        self.input_text_css_selector = "//input[@type='text']"
        self.password_css_selector = "//input[@placeholder='Hasło']"
        self.submit_button_selector = "//button[@type='submit']"
        self.wait = WebDriverWait(driver, 10)

    def close_cookie_term(self) -> None:
        button = driver.find_element(By.CSS_SELECTOR, self.cookie_term_css_selector)
        button.click()

    def facebook_login(self) -> None:
        user_name = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.input_text_css_selector))
        )
        password = driver.find_element(By.XPATH, self.password_css_selector)

        user_name.send_keys(self.email)
        password.send_keys(self.password)

        log_in_button = driver.find_element(By.XPATH, self.submit_button_selector)
        log_in_button.click()

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']"))
        )

    def security_code(self) -> None:
        security_code_input = driver.find_elements(
            By.XPATH, self.input_text_css_selector
        )
        if security_code_input:
            security_code = input("Enter your security code: ")
            security_code_input[0].send_keys(security_code)

        save_button = driver.find_element(By.XPATH, self.submit_button_selector)
        save_button.click()

    def save_browser(self) -> None:
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']"))
        )
        continue_button = driver.find_element(By.XPATH, self.submit_button_selector)
        continue_button.click()

    @staticmethod
    def save_cookies() -> None:
        cookies = driver.get_cookies()
        with open("cookies.json", "wb") as file:
            pickle.dump(cookies, file)

    def login(self):
        # TODO pipeline to run all methods to log in
        pass
