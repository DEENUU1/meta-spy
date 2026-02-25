import re
import time
from typing import List, Dict
from rich import print as rprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..facebook_base import BaseFacebookScraper
from ..scroll import scroll_page_callback
from ...logs import Logs
from ...repository import person_repository, friend_repository, crawlerqueue_repository
from ...utils import output, save_to_json

logs = Logs()

class AccountFriend(BaseFacebookScraper):
    """
    Scraper for Facebook friends list with 'Anchor' logic and total count extraction.
    """

    def __init__(self, user_id: str, crawler: bool = False) -> None:
        super().__init__(
            user_id, base_url=f"https://www.facebook.com/{user_id}/friends"
        )
        self.success = False
        self.crawler = crawler
        self.number_of_friends = 0

    def _load_cookies_and_refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._load_cookies()

    @property
    def is_pipeline_successful(self) -> bool:
        return self.success

    def scrape_friend_count(self) -> int:
        """Finds the total friend count from the page text."""
        try:
            # Wait for the friends header to render
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'friends')]"))
            )
            
            # Scroll slightly to ensure elements are in view
            self._driver.execute_script("window.scrollTo(0, 350);")
            time.sleep(2)

            page_text = self._driver.find_element(By.TAG_NAME, "body").text
            match = re.search(r'(\d{1,3}(?:,\d{3})*)\s+friends', page_text)
            
            if match:
                count_str = match.group(1).replace(',', '')
                count = int(count_str)
                rprint(f"[bold green]✓ Page Scrape: Found {count} total friends.[/bold green]")
                return count
        except Exception as e:
            logs.log_error(f"Count scrape failed: {e}")
        return 0

    def extract_friends_data(self) -> List[Dict[str, str]]:
        """Return a list of usernames and URLs if the list is public."""
        extracted_elements = []
        try:
            def extract_callback(driver):
                try:
                    main_div = self._driver.find_element(
                        By.CSS_SELECTOR, "div.xyamay9.x1pi30zi.x1l90r2v.x1swvt13"
                    )
                    elements = main_div.find_elements(By.CSS_SELECTOR, "a.x1i10hfl span")
                    for element in elements:
                        username = element.text.strip()
                        url = element.find_element(By.XPATH, "..").get_attribute("href")
                        if username == "" or url is None:
                            continue
                        element_data = {"username": username, "url": url}
                        if element_data not in extracted_elements:
                            rprint(f"Extracted friend: {username}")
                            extracted_elements.append(element_data)
                except:
                    pass

            scroll_page_callback(self._driver, extract_callback)
        except Exception as e:
            logs.log_error(f"Error extracting friends data: {e}")

        return extracted_elements

    def pipeline(self) -> None:
        try:
            # --- ANCHOR CHECK: Ensure we aren't redirected to the home feed ---
            if self._user_id not in self._driver.current_url:
                rprint(f"[bold yellow]⚠ Redirect detected. Forcing browser back to {self._user_id}...[/bold yellow]")
                self._driver.get(f"https://www.facebook.com/{self._user_id}/friends")
                time.sleep(5) 

            # 1. Scrape the count (e.g., 323)
            self.number_of_friends = self.scrape_friend_count()

            if not person_repository.person_exists(self._user_id):
                person_repository.create_person(self._user_id)
            person_id = person_repository.get_person(self._user_id).id

            # 2. Update the Database with the total number
            person_repository.update_number_of_friends(person_id, self.number_of_friends)
            rprint(f"[bold cyan]📊 Database: Set total friends to {self.number_of_friends} for {self._user_id}[/bold cyan]")

            rprint("[bold]Step 2 of 2 - Extracting friends list[/bold]")
            extracted_data = self.extract_friends_data()
            
            if not any(extracted_data):
                if self._user_id in self._driver.current_url:
                    rprint("[bold yellow]⚠ List is hidden. Only the total count was saved.[/bold yellow]")
                else:
                    rprint("[bold red]❌ Error: Browser drifted off the profile page.[/bold red]")
            else:
                save_to_json.SaveJSON(self._user_id, extracted_data).save()
                added_count = 0
                for data in extracted_data:
                    if self.crawler:
                        if not crawlerqueue_repository.crawler_queue_exists(data["url"]):
                            crawlerqueue_repository.create_crawler_queue(data["url"])
                    if not friend_repository.friend_exists(person_id, data["username"], data["url"]):
                        friend_repository.create_friends(data["username"], data["url"], person_id)
                        added_count += 1
                rprint(f"[bold green]✅ Success: Added {added_count} new friends to database.[/bold green]")

            self._driver.quit()
            self.success = True

        except Exception as e:
            logs.log_error(f"Pipeline error: {e}")
            rprint(f"[bold red]An error occurred: {e}[/bold red]")
            
            