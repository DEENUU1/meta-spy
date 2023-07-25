import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from config import Config
from scraper import Scraper


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FacebookLogIn(Scraper):
    """
    Log in to Facebook using email and password
    """

    def __init__(self) -> None:
        super().__init__()
        self._base_url = "https://www.facebook.com/"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver = self._driver
        self._driver.get(self._base_url)
        self._cookie_term_css_selector = "._42ft._4jy0._al65._4jy3._4jy1.selected._51sy"
        self._input_text_css_selector = "//input[@type='text']"
        self._password_css_selector = "//input[@placeholder='Hasło']"
        self._submit_button_selector = "//button[@type='submit']"
        self._wait = WebDriverWait(self._driver, 10)

    def _close_cookie_term(self) -> None:
        """
        Close modal with cookie information
        """
        try:
            button = self._driver.find_element(
                By.CSS_SELECTOR, self._cookie_term_css_selector
            )
            button.click()
        except Exception as e:
            logging.error(f"Error occurred while closing cookie modal: {e}")

    def _facebook_login(self) -> None:
        """
        Log in to Facebook using email and password
        """
        try:
            user_name = self._wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self._input_text_css_selector)
                )
            )
            password = self._driver.find_element(By.XPATH, self._password_css_selector)

            user_name.send_keys(Config.FACEBOOK_EMAIL)
            password.send_keys(Config.FACEBOOK_PASSWORD)

            log_in_button = self._driver.find_element(
                By.XPATH, self._submit_button_selector
            )
            log_in_button.click()

            self._wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Facebook']")
                )
            )
        except Exception as e:
            logging.error(f"Error occurred while logging in: {e}")

    def _security_code(self) -> None:
        """
        Add security code for 2-step verification of email and password
        """
        try:
            security_code_input = self._driver.find_elements(
                By.XPATH, self._input_text_css_selector
            )
            if security_code_input:
                security_code = input("Enter your security code: ")
                security_code_input[0].send_keys(security_code)

            save_button = self._driver.find_element(
                By.XPATH, self._submit_button_selector
            )
            save_button.click()
        except Exception as e:
            logging.error(f"Error occurred while adding security code: {e}")

    def _save_browser(self) -> None:
        """
        Click button to save browser
        """
        try:
            self._wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Facebook']")
                )
            )
            continue_button = self._driver.find_element(
                By.XPATH, self._submit_button_selector
            )
            continue_button.click()
        except Exception as e:
            logging.error(f"Error occurred while saving browser: {e}")

    def _save_cookies(self) -> None:
        """
        Save cookies with log in account to json file
        """
        try:
            cookies = self._driver.get_cookies()
            with open(Config.COOKIES_FILE_PATH, "wb") as file:
                pickle.dump(cookies, file)
        except Exception as e:
            logging.error(f"Error occurred while saving cookies: {e}")

    def login_2_step(self) -> None:
        """
        Pipeline to log in on an account with 2-step verification
        """
        self._close_cookie_term()
        self._facebook_login()
        self._security_code()
        self._save_browser()
        self._save_cookies()

    def login_no_verification(self) -> None:
        """
        Pipeline to log in on an account without 2-step verification
        """
        self._close_cookie_term()
        self._facebook_login()
        self._save_browser()
        self._save_cookies()
