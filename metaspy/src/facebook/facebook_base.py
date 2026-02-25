import time
import pickle
from rich import print as rprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from .scraper import Scraper
from ..config import Config
from ..logs import Logs

logs = Logs()

class BaseFacebookScraper(Scraper):
    def __init__(self, user_id: str, base_url: str) -> None:
        super().__init__()
        # 1. Clean and lock the user ID
        self._user_id = str(user_id).strip()
        
        # 2. Build the literal URL to protect dots in usernames like debbi.wood
        if "{user_id}" in base_url or "{}" in base_url:
            self._base_url = f"https://www.facebook.com/{self._user_id}"
        else:
            self._base_url = base_url

        # 3. Initialize the driver
        self._driver = webdriver.Chrome(options=self._chrome_driver_configuration())
        self._load_cookies()
        
        # 4. First navigation attempt
        rprint(f"[bold blue]🚀 Navigating to {self._user_id}...[/bold blue]")
        self._driver.get(self._base_url)
        time.sleep(5) # Essential wait for FB redirection to settle

        # 5. THE ANCHOR: This is what triggers the "Force anchoring" message
        current_url = self._driver.current_url.lower()
        target_id = self._user_id.lower()

        if target_id not in current_url:
            rprint(f"[bold red]⚠ Drift detected (Landed on: {current_url}). Force-anchoring to {target_id}...[/bold red]")
            # Force the browser back to the specific profile page
            self._driver.get(self._base_url)
            time.sleep(7) # Heavier wait for the second attempt
            
            # Final check to warn if Facebook is totally blocking the redirect
            if target_id not in self._driver.current_url.lower():
                rprint("[bold red]❌ Critical: Browser is stuck on your feed. Facebook is blocking the automated redirect to this profile.[/bold red]")
        
        self._wait = WebDriverWait(self._driver, 10)
        self.success = False

    def _load_cookies(self) -> None:
        """Loads Firefox session cookies to bypass login screens"""
        try:
            # This calls the Firefox session injector we built into scraper.py
            super()._load_cookies()
        except Exception as e:
            logs.log_error(f"Cookie loading failed: {e}")
            
            