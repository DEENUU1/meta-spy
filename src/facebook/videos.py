import logging
import pickle
from time import sleep
from typing import List

from config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scraper import Scraper
from rich import print


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FacebookVideoScraper(Scraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = f"https://www.facebook.com/{self._user_id}/videos"
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 10)
        self.success = False

    def _load_cookies(self) -> None:
        """
        Load cookies with a log in session
        """
        print("🍪Loading cookies🍪")
        try:
            self._driver.delete_all_cookies()
            with open(Config.COOKIES_FILE_PATH, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        logging.error(f"Error adding cookie: {cookie}, Exception: {e}")
                        print("❗Loading cookies failed❗")

        except Exception as e:
            logging.error(f"Error loading cookies: {e}")
            print("❗Loading cookies failed❗")

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
        print("🏎️Scrolling page🏎️")
        try:
            last_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            consecutive_scrolls = 0

            while consecutive_scrolls < Config.MAX_CONSECUTIVE_SCROLLS:
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                sleep(Config.SCROLL_PAUSE_TIME)
                new_height = self._driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height

        except Exception as e:
            logging.error(f"Error occurred while scrolling: {e}")
            print("❗Page scrolling failed❗")

    def extract_videos_urls(self) -> List[str]:
        """
        Return a list of all the image urls
        """
        extracted_videos_urls = []
        print("🖼️Start extracting videos URLs🖼️")
        try:
            videos_elements = self._driver.find_elements(
                By.CSS_SELECTOR,
                "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv",
            )
            for video_element in videos_elements:
                src_attribute = video_element.get_attribute("href")
                if src_attribute:
                    extracted_videos_urls.append(src_attribute)

        except Exception as e:
            logging.error(f"Error extracting reels URLs: {e}")
            print("❗Extracting reels  URLs failed❗")

        return extracted_videos_urls

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            self._load_cookies()
            self._driver.refresh()
            self.scroll_page()
            videos = self.extract_videos_urls()

            print(videos)

            self._driver.quit()

            self.success = True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
