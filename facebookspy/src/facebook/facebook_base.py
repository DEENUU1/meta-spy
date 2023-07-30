import logging
import pickle

from ..config import Config
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from .scraper import Scraper


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class BaseFacebookScraper(Scraper):
    def __init__(self, user_id, base_url) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = base_url.format(self._user_id)
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)
        self.success = False

    def _load_cookies(self) -> None:
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")

        except Exception as e:
            logging.error(f"Error loading cookies: {e}")
