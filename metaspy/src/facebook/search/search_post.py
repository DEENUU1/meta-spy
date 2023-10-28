from rich import print as rprint
from ...logs import Logs
from selenium.webdriver.common.by import By
from typing import List
from ..scroll import scroll_page_callback
from selenium.webdriver.common.action_chains import ActionChains
from .search_base import SearchBase


logs = Logs()


class SearchPost(SearchBase):
    def __init__(self, query: str, max_result: int):
        super().__init__(query, max_result)

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

    @staticmethod
    def _extract_url_prefix(url: str) -> str:
        """Return only the first part of url to avoid creating duplicates"""
        index = url.find("[0]")
        if index != -1:
            return url[:index]
        return url

    def scrape_data(self) -> List[str]:
        """
        Return a list of posts
        """
        excracted_elements = []
        url = self.get_url("posts")

        try:
            self.load_driver(url)

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

                    if len(excracted_elements) + 1 >= self.max_result:
                        self._driver.quit()
                        self.success = True

                    if parsed_url not in excracted_elements:
                        rprint(f"Extracted post: {parsed_url}")
                        excracted_elements.append(parsed_url)

                    self._move_cursor_away()

            scroll_page_callback(self._driver, extract_callback)

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")

        return excracted_elements
