from ..facebook.scraper import Scraper
import pickle
from rich import print as rprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from ..config import Config
from ..logs import Logs

logs = Logs()
config = Config()


class BaseInstagramScraper(Scraper):
    def __init__(self, user_id: str, base_url: str) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = base_url.format(self._user_id)
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)
        self.success = False

    @staticmethod
    def _check_session_id() -> bool:
        check = config.INSTAGRAM_SESSIONID_VALUE == True
        if not check:
            rprint(f"[bold red] Add you sessionid key to .env fil e[/bold red]")
            return False
        else:
            return True
