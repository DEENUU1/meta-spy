from time import sleep
from typing import List, Dict

from ...config import Config
from selenium.webdriver.common.by import By
from ...repository import person_repository, friend_repository
from ..facebook_base import BaseFacebookScraper
from ...logs import Logs
from rich import print as rprint


logs = Logs()


class AccountFriend(BaseFacebookScraper):
    """
    Scrape user's friends list
    """

    def __init__(self, user_id) -> None:
        super().__init__(
            user_id, base_url=f"https://www.facebook.com/{user_id}/friends"
        )
        self.success = False

    def extract_friends_data(self) -> List[Dict[str, str]]:
        """
        Return a list of dictionaries with the usernames and the urls to the profile for every person in friends list
        """
        extracted_elements = []
        try:
            elements = self._driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl span")
            for element in elements:
                username = element.text.strip()
                url = element.find_element(By.XPATH, "..").get_attribute("href")
                if username == "":
                    continue
                element_data = {"username": username, "url": url}
                extracted_elements.append(element_data)

        except Exception as e:
            logs.log_error(f"Error extracting friends data: {e}")

        return extracted_elements

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
                self.extract_friends_data()
                new_height = self._driver.execute_script(
                    "return document.body.scrollHeight"
                )

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height
        except Exception as e:
            logs.log_error(f"Error occurred while scrolling: {e}")

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 4 - Load cookies[/bold]")
            self._load_cookies()
            rprint("[bold]Step 2 of 3 - Refresh driver[/bold]")
            self._driver.refresh()
            rprint("[bold]Step 3 of 4 - Scrolling page[/bold]")
            self.scroll_page()

            rprint("[bold]Step 4 of 4 - Extracting friends data[/bold]")
            extracted_data = self.extract_friends_data()
            rprint(extracted_data)

            if not person.person_exists(self._user_id):
                person.create_person(self._user_id)

            person_object = person.get_person(self._user_id).id

            for data in extracted_data:
                if not friend.friend_exists(person_id, data["username"], data["url"]):
                    friend.create_friends(data["username"], data["url"], person_object)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
