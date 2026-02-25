import time
from typing import List
from rich import print as rprint
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page_callback
from ...logs import Logs
from ...repository import person_repository, post_repository
from ...utils import output, save_to_json

logs = Logs()

class AccountPost(BaseFacebookScraper):
    def __init__(self, user_id: str) -> None:
        super().__init__(user_id, base_url=f"https://www.facebook.com/{user_id}/")
        self.success = False

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    @staticmethod
    def _extract_url_prefix(url: str) -> str:
        index = url.find("[0]")
        return url[:index] if index != -1 else url

    def _perform_hover_action(self, element) -> None:
        try:
            actions = ActionChains(self._driver)
            actions.move_to_element(element)
            actions.perform()
        except: pass

    def _move_cursor_away(self) -> None:
        try:
            actions = ActionChains(self._driver)
            actions.move_by_offset(0, 0).perform()
        except: pass

    def extract_post_urls(self) -> List[str]:
        extracted_urls = []
        try:
            def extract_callback(driver):
                # BROAD SELECTOR: Catches native posts and shared external links (TikTok)
                # It looks for standard Facebook link patterns in timeline articles
                selectors = [
                    "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm",
                    "div[role='article'] a[href*='/posts/']",
                    "div[role='article'] a[href*='facebook.com/photo']"
                ]
                
                for selector in selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        actual_url = element.get_attribute("href")
                        if not actual_url: continue
                        
                        parsed_url = self._extract_url_prefix(actual_url)
                        if parsed_url.endswith("#") or "facebook.com/l.php" in parsed_url:
                            continue
                            
                        if parsed_url not in extracted_urls:
                            rprint(f"🔗 Found: {parsed_url}")
                            extracted_urls.append(parsed_url)

            scroll_page_callback(self._driver, extract_callback)
        except Exception as e:
            logs.log_error(f"Error extracting post URLs: {e}")
        return extracted_urls

    def pipeline(self) -> None:
        try:
            # Step 1: Extract data (cookies handled by Base class __init__)
            rprint("[bold]Step 2 of 2 - Extracting post urls[/bold]")
            extracted_data = self.extract_post_urls()

            if not extracted_data:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                rprint(f"[bold red]Saving {len(extracted_data)} posts to database...[/bold red]")
                
                save_to_json.SaveJSON(self._user_id, extracted_data).save()

                if not person_repository.person_exists(self._user_id):
                    person_repository.create_person(self._user_id)
                person_id = person_repository.get_person(self._user_id).id

                added_count = 0
                for data in extracted_data:
                    if not post_repository.post_exists(data):
                        post_repository.create_post(data, person_id)
                        added_count += 1

                rprint(f"[bold green]✅ Success: Found {len(extracted_data)} total posts. Added {added_count} new records.[/bold green]")
                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")
            
            