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


class FacebookLogIn:
    """
    Log in to Facebook using email and password
    """

    def __init__(self) -> None:
        self.email = os.getenv("FACEBOOK_EMAIL")
        self.password = os.getenv("FACEBOOK_PASSWORD")
        self.base_url = "https://www.facebook.com/"
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = self.driver
        self.driver.get(self.base_url)
        self.cookie_term_css_selector = "._42ft._4jy0._al65._4jy3._4jy1.selected._51sy"
        self.input_text_css_selector = "//input[@type='text']"
        self.password_css_selector = "//input[@placeholder='Hasło']"
        self.submit_button_selector = "//button[@type='submit']"
        self.wait = WebDriverWait(self.driver, 10)

    def close_cookie_term(self) -> None:
        """
        Close modal with cookie information
        """
        button = self.driver.find_element(
            By.CSS_SELECTOR, self.cookie_term_css_selector
        )
        button.click()

    def facebook_login(self) -> None:
        """
        Log in to Facebook using email and password
        """
        user_name = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.input_text_css_selector))
        )
        password = self.driver.find_element(By.XPATH, self.password_css_selector)

        user_name.send_keys(self.email)
        password.send_keys(self.password)

        log_in_button = self.driver.find_element(By.XPATH, self.submit_button_selector)
        log_in_button.click()

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']"))
        )

    def security_code(self) -> None:
        """
        Add security code for 2-step verification of email and password
        """
        security_code_input = self.driver.find_elements(
            By.XPATH, self.input_text_css_selector
        )
        if security_code_input:
            security_code = input("Enter your security code: ")
            security_code_input[0].send_keys(security_code)

        save_button = self.driver.find_element(By.XPATH, self.submit_button_selector)
        save_button.click()

    def save_browser(self) -> None:
        """
        Click button to save browser
        """
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']"))
        )
        continue_button = self.driver.find_element(
            By.XPATH, self.submit_button_selector
        )
        continue_button.click()

    def save_cookies(self) -> None:
        """
        Save cookies with log in account to json file
        """
        cookies = self.driver.get_cookies()
        with open("cookies.json", "wb") as file:
            pickle.dump(cookies, file)

    def login_2_step(self):
        self.close_cookie_term()
        self.facebook_login()
        self.security_code()
        self.save_browser()
        self.save_cookies()
