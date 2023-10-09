from typing import List

from rich import print as rprint
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page_callback
from ...logs import Logs
from ...repository import person_repository, post_repository
from ...utils import output

logs = Logs()


class AccountPost(BaseFacebookScraper):
    """
    Scrape user's friends list
    """

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/")
        self.success = False

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()
        self._driver.refresh()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    @staticmethod
    def _extract_url_prefix(url: str) -> str:
        """Return only the first part of url to avoid creating duplicates"""
        index = url.find("[0]")
        if index != -1:
            return url[:index]
        return url

    def _perform_hover_action(self, element) -> None:
        """
        Perform a hover action on the given element
        """
        try:
            actions = ActionChains(self._driver)
            actions.move_to_element(element)
            actions.perform()
        except Exception as e:
            logs.log_error(f"Error performing hover action: {e}")

    def _move_cursor_away(self) -> None:
        """
        Move the cursor away from any element
        """
        actions = ActionChains(self._driver)
        actions.move_by_offset(0, 0).perform()

    def extract_post_urls(self) -> List[str]:
        """
        Return a list urls for posts from facebook account
        """
        extracted_urls = []
        try:

            def extract_callback(driver):
                elements = driver.find_elements(
                    By.CSS_SELECTOR,
                    "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm",
                )
                for element in elements:
                    self._perform_hover_action(element)

                    actual_url = element.get_attribute("href")
                    parsed_url = self._extract_url_prefix(actual_url)
                    if parsed_url.endswith("#"):
                        continue
                    if parsed_url not in extracted_urls:
                        rprint(f"Extracted URL: {parsed_url}")

                        extracted_urls.append(parsed_url)

                    self._move_cursor_away()

            scroll_page_callback(self._driver, extract_callback)

        except Exception as e:
            logs.log_error(f"Error extracting post URLs: {e}")

        return extracted_urls

    def pipeline(self) -> None:
        """
        Pipeline to run the scraper
        """
        try:
            rprint("[bold]Step 1 of 2 - Load cookies[/bold]")
            self._load_cookies_and_refresh_driver()

            rprint("[bold]Step 2 of 2 - Extracting post urls[/bold]")
            extracted_data = self.extract_post_urls()

            if not extracted_data:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                output.print_list(extracted_data)

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)

                person_id = person_repository.get_person(self._user_id).id

                for data in extracted_data:
                    if not post_repository.post_exists(data):
                        post_repository.create_post(data, person_id)

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
