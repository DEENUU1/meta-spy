import logging
from time import sleep
from typing import List, Dict

from ..facebook_base import BaseFacebookScraper
from ...config import Config
from selenium.webdriver.common.by import By
from rich import print as rprint
from ...repository import create_person, get_person, person_exists, create_recent_places


# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FacebookRecentPlaces(BaseFacebookScraper):
    """
    Scrape user's pictures
    """

    def __init__(self, user_id) -> None:
        super().__init__(
            user_id, base_url=f"https://www.facebook.com/{user_id}/places_recent"
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

    def extract_recent_places(self) -> List[Dict[str, str]]:
        """
        Return data about recent places
        """
        extracted_image_urls = []
        try:
            data = {}
            div_element = self._driver.find_element(
                By.CSS_SELECTOR,
                "div.xyamay9.x1pi30zi.x1l90r2v.x1swvt13",
            )
            span_elements = div_element.find_elements(
                By.CSS_SELECTOR,
                "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u",
            )

            div_inside_elements = div_element.find_elements(
                By.CSS_SELECTOR, "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs"
            )

            for i in range(len(span_elements)):
                data = {}
                data["localization"] = span_elements[i].text
                data["date"] = div_inside_elements[i].text

                extracted_image_urls.append(data)

            extracted_image_urls.append(data)
        except Exception as e:
            logging.error(f"Error extracting image URLs: {e}")

        return extracted_image_urls

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
            recent_places = self.extract_recent_places()
            rprint(recent_places)

            if not person_exists(self._user_id):
                create_person(self._user_id)

            person_id = get_person(self._user_id).id

            for place in recent_places:
                create_recent_places(place["localization"], place["date"], person_id)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logging.error(f"An error occurred: {e}")
