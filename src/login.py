import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from config import Config

# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Chrome configuration
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
        self.config = Config()
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
        try:
            button = self.driver.find_element(
                By.CSS_SELECTOR, self.cookie_term_css_selector
            )
            button.click()
        except Exception as e:
            logging.error(f"Error occurred while closing cookie modal: {e}")

    def facebook_login(self) -> None:
        """
        Log in to Facebook using email and password
        """
        try:
            user_name = self.wait.until(
                EC.presence_of_element_located((By.XPATH, self.input_text_css_selector))
            )
            password = self.driver.find_element(By.XPATH, self.password_css_selector)

            user_name.send_keys(self.config.FACEBOOK_EMAIL)
            password.send_keys(self.config.FACEBOOK_PASSWORD)

            log_in_button = self.driver.find_element(
                By.XPATH, self.submit_button_selector
            )
            log_in_button.click()

            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Facebook']")
                )
            )
        except Exception as e:
            logging.error(f"Error occurred while logging in: {e}")

    def security_code(self) -> None:
        """
        Add security code for 2-step verification of email and password
        """
        try:
            security_code_input = self.driver.find_elements(
                By.XPATH, self.input_text_css_selector
            )
            if security_code_input:
                security_code = input("Enter your security code: ")
                security_code_input[0].send_keys(security_code)

            save_button = self.driver.find_element(
                By.XPATH, self.submit_button_selector
            )
            save_button.click()
        except Exception as e:
            logging.error(f"Error occurred while adding security code: {e}")

    def save_browser(self) -> None:
        """
        Click button to save browser
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Facebook']")
                )
            )
            continue_button = self.driver.find_element(
                By.XPATH, self.submit_button_selector
            )
            continue_button.click()
        except Exception as e:
            logging.error(f"Error occurred while saving browser: {e}")

    def save_cookies(self) -> None:
        """
        Save cookies with log in account to json file
        """
        try:
            cookies = self.driver.get_cookies()
            with open(self.config.COOKIES_FILE_PATH, "wb") as file:
                pickle.dump(cookies, file)
        except Exception as e:
            logging.error(f"Error occurred while saving cookies: {e}")


def login_2_step(facebook: FacebookLogIn) -> None:
    """
    Pipeline to log in on an account with 2-step verification
    """
    facebook.close_cookie_term()
    facebook.facebook_login()
    facebook.security_code()
    facebook.save_browser()
    facebook.save_cookies()


def login_no_verification(facebook: FacebookLogIn) -> None:
    """
    Pipeline to log in on an account without 2-step verification
    """
    facebook.close_cookie_term()
    facebook.facebook_login()
    facebook.save_browser()
    facebook.save_cookies()
