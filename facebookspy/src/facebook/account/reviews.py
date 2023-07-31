import logging
from time import sleep
from typing import List, Dict

from ...config import Config
from selenium.webdriver.common.by import By
from rich import print as rprint
from ..facebook_base import BaseFacebookScraper
from ...repository import create_person, get_person, person_exists, create_reviews


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FacebookReviewsScraper(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__(
            user_id, base_url=f"https://www.facebook.com/{user_id}/reviews_written"
        )
        self.success = False

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more friends from a list
        """
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
            rprint(reviews)

            if not person_exists(self._user_id):
                create_person(self._user_id)

            person_id = get_person(self._user_id)

            for review in reviews:
                create_reviews(review["company"], review["opinions"], person_id)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logging.error(f"An error occurred: {e}")
