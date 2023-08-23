import pickle

from rich import print as rprint
from rich.prompt import Prompt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .scraper import Scraper
from ..config import Config
from ..logs import Logs

logs = Logs()


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
        self._password_css_selector = "//input[@type='password']"
        self._submit_button_selector = "//button[@type='submit']"
        self._wait = WebDriverWait(self._driver, 10)
        self.success = False

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
            logs.log_error(f"An error occurred while closing cookie term {e}")

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
            logs.log_error(f"An Error occurred while logging in: {e}")

    def _security_code(self, security_code) -> None:
        """
        Add security code for 2-step verification of email and password
        """
        try:
            security_code_input = self._driver.find_elements(
                By.XPATH, self._input_text_css_selector
            )
            if security_code_input:
                security_code_input[0].send_keys(security_code)

            save_button = self._driver.find_element(
                By.XPATH, self._submit_button_selector
            )
            save_button.click()
        except Exception as e:
            logs.log_error(f"An Error occurred while adding security code: {e}")

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
            logs.log_error(f"An Error occurred while saving browser: {e}")

    def _save_cookies(self) -> None:
        """
        Save cookies with log in account to json file
        """
        try:
            cookies = self._driver.get_cookies()
            with open(Config.COOKIES_FILE_PATH, "wb") as file:
                pickle.dump(cookies, file)
        except Exception as e:
            logs.log_error(f"An Error occurred while saving cookies: {e}")

    @property
    def is_pipeline_successful(self) -> bool:
        """
        Check if pipeline was successful
        """
        return self.success

    def login_2_step_pipeline(self) -> None:
        """
        Pipeline to log in on an account with 2-step verification
        """
        try:
            rprint("Step 1 of 5 - Closing cookie term modal")
            self._close_cookie_term()
            rprint("Step 2 of 5 - Logging in")
            self._facebook_login()
            security_code = Prompt.ask("🔒Security code")
            rprint("Step 3 of 5 - Adding security code")
            self._security_code(security_code)
            rprint("Step 4 of 5 - Saving browser")
            self._save_browser()
            rprint("Step 5 of 5 - Saving cookies")
            self._save_cookies()

            self.success = True

        except Exception as e:
            logs.log_error(f"An Error occurred while logging in: {e}")
            rprint(f"An Error occurred while logging in {e}")

    def login_no_verification_pipeline(self) -> None:
        """
        Pipeline to log in on an account without 2-step verification
        """
        try:
            rprint("Step 1 of 4 - Closing cookie term modal")
            self._close_cookie_term()
            rprint("Step 2 of 4 - Logging in")
            self._facebook_login()
            rprint("Step 3 of 4 - Saving browser")
            self._save_browser()
            rprint("Step 4 of 4 - Saving cookies")
            self._save_cookies()

            self.success = True

        except Exception as e:
            logs.log_error(f"An Error occurred while logging in: {e}")
            rprint(f"An Error occurred while logging in {e}")
