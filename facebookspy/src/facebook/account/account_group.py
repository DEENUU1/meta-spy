from time import sleep
from typing import List, Dict

from ...config import Config
from selenium.webdriver.common.by import By
from ...repository import person_repository, group_repository
from ..facebook_base import BaseFacebookScraper
from ...logs import Logs
from rich import print as rprint


logs = Logs()


class AccountGroup(BaseFacebookScraper):
    """
    Scrape user's groups
    """

    def __init__(self, user_id) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/groups")
        self.success = False

    def extract_groups_data(self) -> List[Dict]:
        extracted_data = []
        try:
            div_element = self._driver.find_element(
                By.CSS_SELECTOR, "div.xyamay9.x1pi30zi.x1l90r2v.x1swvt13"
            )

            group_elements = div_element.find_elements(
                By.CSS_SELECTOR, "a.x1i10hfl span"
            )

            for element in group_elements:
                name = element.text.strip()
                url = element.find_element(By.XPATH, "..").get_attribute("href")
                if name == "":
                    continue

                extracted_data.append({"name": name, "url": url})

        except Exception as e:
            logs.log_error(f"Error extracting data: {e}")

        return extracted_data

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more data from a website
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
                self.extract_groups_data()
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

            rprint("[bold]Step 4 of 4 - Extracting likes data[/bold]")
            extracted_data = self.extract_groups_data()
            rprint(extracted_data)

            rprint(
                "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
            )

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)

            person_id = person_repository.get_person(self._user_id).id

            for data in extracted_data:
                if not group_repository.group_exists(data["name"]):
                    group_repository.create_group(person_id, data["name"], data["url"])

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
