from ..scraper import Scraper
from ...config import Config
import pickle
from rich import print as rprint
from ...logs import Logs
from selenium import webdriver
from typing import List
from abc import abstractmethod, ABC
from ...utils.save_to_json import SaveJSON

logs = Logs()


class SearchBase(Scraper, ABC):
    def __init__(self, query: str, max_result: int):
        super().__init__()
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self.query = query
        self.max_result = max_result
        self.base_url = "https://www.facebook.com/search/"
        self.success = False

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def _load_cookies(self) -> None:
        """Load cookies with log in session"""
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

    def get_url(self, subpage) -> str:
        return f"{self.base_url}{subpage}?q={self.query}"

    def load_driver(self, url) -> None:
        self._driver.get(url)
        self._load_cookies()
        self._driver.refresh()

    @abstractmethod
    def scrape_data(self) -> List[str]:
        """
        Return a list of urls
        """
        pass

    def pipeline(self) -> None:
        rprint(f"[bold]Start searching for query: {self.query}[/bold]")

        scraped_data = self.scrape_data()
        if scraped_data:
            rprint(
                "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
            )

            SaveJSON(facebook_id=self.query, data=scraped_data).save()
            self.success = True

        else:
            self.success = False
