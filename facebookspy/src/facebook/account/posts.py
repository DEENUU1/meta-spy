from time import sleep
from typing import List, Dict
from selenium.webdriver.common.action_chains import ActionChains

from ...config import Config
from selenium.webdriver.common.by import By
from ...repository import person, post
from ..facebook_base import BaseFacebookScraper
from ...logs import Logs
from rich import print as rprint


logs = Logs()


class PostScraper(BaseFacebookScraper):
    """
    Scrape user's friends list
    """

    def __init__(self, user_id) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/")
        self.success = False

    def extract_post_urls(self) -> List[str]:
        """
        Return a list urls for posts from facebook account
        """
        extracted_urls = []
        try:
            elements = self._driver.find_elements(
                By.CSS_SELECTOR,
                "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm",
            )
            for element in elements:
                self._perform_hover_action(element)

                actual_url = element.get_attribute("href")

                extracted_urls.append(actual_url)

                self._move_cursor_away()

        except Exception as e:
            logs.log_error(f"Error extracting post URLs: {e}")

        return extracted_urls

    def _perform_hover_action(self, element) -> None:
        """
        Perform a hover action on the given element
        """
        actions = ActionChains(self._driver)
        actions.move_to_element(element).perform()

    def _move_cursor_away(self) -> None:
        """
        Move the cursor away from any element
        """
        actions = ActionChains(self._driver)
        actions.move_by_offset(0, 0).perform()

    def scroll_page(self) -> None:
        """
        Scrolls the page to load more posts from facebook acccount
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

            rprint("[bold]Step 4 of 4 - Extracting post urls[/bold]")
            extracted_data = self.extract_post_urls()
            rprint(extracted_data)

            if not person.person_exists(self._user_id):
                person.create_person(self._user_id)

            person_id = person.get_person(self._user_id).id

            for data in extracted_data:
                if not post.post_exists(data):
                    post.create_post(data, person_id)

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
