from time import sleep
from typing import List, Dict
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from ..config import Config
from selenium.webdriver.common.by import By
from ..repository import person, post
from ..logs import Logs
from rich import print as rprint
from .scraper import Scraper
import pickle

logs = Logs()


class PostDetailScraper(Scraper):
    """
    Scrape detail of Post
    """

    def __init__(self, user_id: int) -> None:
        super().__init__()
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._user_id = user_id
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
                        logs.log_error(f"An Error occurred adding cookies {e}")
                        rprint(f"An Error occurred while adding cookies {e}")

        except Exception as e:
            logs.log_error(f"An Error occurred while loading cookies: {e}")
            rprint(f"An Error occurred while loading cookies {e}")

    def scrape_post_data(self, url: str):
        try:
            self._driver.get(url)

        except Exception as e:
            logs.log_error(f"Error occurred while loading post detail page: {e}")

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            # rprint("[bold]Step 1 of 4 - Load cookies[/bold]")
            self._load_cookies()
            # rprint("[bold]Step 2 of 3 - Refresh driver[/bold]")
            self._driver.refresh()

            extracted_data = self.scrape_post_data()
            rprint(extracted_data)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
