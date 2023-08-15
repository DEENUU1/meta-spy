from time import sleep
from typing import List, Dict
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from ..config import Config
from selenium.webdriver.common.by import By
from ..repository import person_repository, post_repository
from ..logs import Logs
from rich import print as rprint
from .scraper import Scraper
import pickle

logs = Logs()


class PostDetail(Scraper):
    """
    Scrape detail of Post
    """

    def __init__(self, user_id: str) -> None:
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

    @staticmethod
    def _extract_number(text: str) -> int | None:
        parts = text.split(" ", 1)
        if len(parts) > 0 and parts[0].isdigit():
            return int(parts[0])
        else:
            return None

    @staticmethod
    def _check_number_is_int(text) -> bool:
        try:
            int(text)
            return True
        except ValueError:
            return False

    def scrape_post_data(self, url: str):
        try:
            self._driver.get(url)
            self._load_cookies()
            self._driver.refresh()

            print("=====POST=====")

            stats_div = self._driver.find_element(
                By.CSS_SELECTOR,
                "div.x6s0dn4.xi81zsa.x78zum5.x6prxxf.x13a6bvl.xvq8zen.xdj266r.xktsk01.xat24cr.x1d52u69.x889kno.x4uap5.x1a8lsjc.xkhd6sd.xdppsyt",
            )

            number_of_likes = stats_div.find_element(
                By.CSS_SELECTOR, "span.xt0b8zv.x1e558r4"
            ).text

            print(number_of_likes)

            comment_share_elements = stats_div.find_elements(
                By.CSS_SELECTOR,
                "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa",
            )

            for element in comment_share_elements:
                if not self._check_number_is_int(element.text):
                    value = self._extract_number(element.text)
                    print(value)

            text_div = self._driver.find_element(
                By.CSS_SELECTOR,
                "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a",
            ).text

            print(text_div)

            img_element = self._driver.find_element(By.CSS_SELECTOR, "img.x1ey2m1c")
            img_url = img_element.get_attribute("src")
            print("Image URL:", img_url)

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

            person_object = person.get_person(self._user_id)
            posts = post.get_posts(person_object.id)

            for data in posts:
                self.scrape_post_data(data.url)
                # rprint(extracted_data)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
