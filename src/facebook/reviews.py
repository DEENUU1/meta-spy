import logging
import pickle
from time import sleep
from typing import List, Dict

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


class FacebookReviewsScraper(Scraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id = user_id
        self._base_url = f"https://www.facebook.com/{self._user_id}/reviews_written"
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

    def extract_reviews(self) -> List[Dict[str, str]]:
        """
        Return data about recent places
        """
        extracted_reviews = []
        print("🖼️Start extracting image URLs🖼️")
        try:
            div_elements = self._driver.find_elements(
                By.CSS_SELECTOR,
                "div.x6s0dn4.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1olyfxc.x9f619.x78zum5.x1e56ztr.xyamay9.x1pi30zi.x1l90r2v.x1swvt13",
            )

            for div_element in div_elements:
                data = {}
                company_element = div_element.find_element(
                    By.CSS_SELECTOR,
                    "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u",
                )
                data["company"] = company_element.text

                div_inside_elements = div_element.find_elements(
                    By.CSS_SELECTOR, "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs"
                )

                opinions = [
                    opinion_element.text for opinion_element in div_inside_elements
                ]
                data["opinions"] = opinions

                extracted_reviews.append(data)
        except Exception as e:
            logging.error(f"Error extracting image URLs: {e}")
            print("❗Extracting image URLs failed❗")

        return extracted_reviews

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
            reviews = self.extract_reviews()
            print(reviews)

            self._driver.quit()

            self.success = True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
