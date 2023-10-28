import pickle

from rich import print as rprint
from rich.prompt import Prompt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ..facebook.login import FacebookLogIn
from ..facebook.scraper import Scraper
from ..config import Config
from ..logs import Logs
from time import sleep


logs = Logs()
config = Config()


class InstagramLogIn(Scraper):
    def __init__(self) -> None:
        super().__init__()
        self._base_url = "https://www.instagram.com/"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver = self._driver
        self._driver.get(self._base_url)
        self._cookie_term_css_selector = "_a9--"
        self._login_with_facebook_css_selector = "_acan._acao._acas._aj1-"

    def _close_cookie_term(self) -> None:
        """
        Close modal with cookie information
        """
        try:
            button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, self._cookie_term_css_selector)
                )
            )
            button.click()
        except Exception as e:
            logs.log_error(f"An error occurred while closing cookie term: {e}")

    def _click_login_with_facebook(self) -> None:
        """
        Click button to log in with facebook auth
        """
        try:
            button = self._driver.find_element(
                By.CSS_SELECTOR, self._login_with_facebook_css_selector
            )
            print(button)
            button.click()
        except Exception as e:
            logs.log_error(f"An error occurred while clicking login with facebook {e}")

    def _save_cookies(self) -> None:
        """
        Save cookies with log in account to json file
        """
        try:
            cookies = self._driver.get_cookies()
            with open(Config.INSTAGRAM_FILE_PATH, "wb") as file:
                pickle.dump(cookies, file)
        except Exception as e:
            logs.log_error(f"An Error occurred while saving cookies: {e}")

    @property
    def is_pipeline_successful(self) -> bool:
        """
        Check if pipeline was successful
        """
        return self.success

    def login_with_facebook(self) -> None:
        try:
            rprint(f"Step 1 of  - Closing cookie term modal")
            self._close_cookie_term()
            rprint(f"Step 2 of  - Clicking login with facebook")
            self._click_login_with_facebook()
            sleep(100)
            # FacebookLogIn().login_2_step_pipeline()
            self._save_cookies()

            self.success = True

        except Exception as e:
            logs.log_error(f"An Error occurred while logging in with facebook: {e}")
            rprint(f"An Error occurred while logging in with facebook {e}")
