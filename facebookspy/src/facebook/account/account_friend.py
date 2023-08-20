from time import sleep
from typing import List, Dict

from ...config import Config
from selenium.webdriver.common.by import By
from ...repository import person_repository, friend_repository
from ..facebook_base import BaseFacebookScraper
from ...logs import Logs
from rich import print as rprint
from ..scroll import scroll_page


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
            scroll_page(self._driver)

            rprint("[bold]Step 4 of 4 - Extracting friends data[/bold]")
            extracted_data = self.extract_friends_data()
            rprint(extracted_data)

            rprint(
                "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
            )

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            for data in extracted_data:
                if not friend_repository.friend_exists(
                    person_id, data["username"], data["url"]
                ):
                    friend_repository.create_friends(
                        data["username"], data["url"], person_id
                    )

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
