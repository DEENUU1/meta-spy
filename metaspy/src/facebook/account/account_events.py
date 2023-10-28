from typing import List, Dict

from rich import print as rprint
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page
from ...logs import Logs
from ...repository import person_repository, event_repository
from ...utils import output, save_to_json

logs = Logs()


class AccountEvents(BaseFacebookScraper):
    """
    Scrape user's events
    """

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/events")
        self.success = False

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def extract_events_data(self) -> List[Dict]:
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

                if url is None:
                    continue

                extracted_data.append({"name": name, "url": url})

        except Exception as e:
            logs.log_error(f"Error extracting data: {e}")

        return extracted_data

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 3 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 3 - Scrolling page[/bold]")
            scroll_page(self._driver)

            rprint("[bold]Step 3 of 3 - Extracting likes data[/bold]")
            extracted_data = self.extract_events_data()

            if not any(extracted_data):
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                output.print_data_from_list_of_dict(extracted_data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                save_to_json.SaveJSON(
                    self._user_id,
                    extracted_data,
                ).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                person_id = person_repository.get_person(self._user_id).id

                for data in extracted_data:
                    if (
                        not event_repository.event_exists(data["name"], person_id)
                        and data["url"] != None
                    ):
                        event_repository.create_event(
                            person_id, data["name"], data["url"]
                        )

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
