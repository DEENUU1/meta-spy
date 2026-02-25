import pickle
import os
from selenium.webdriver.chrome.options import Options
from rich import print as rprint
from ..config import Config

class Scraper:
    """
    Base class for web scrapers.
    """

    @staticmethod
    def _chrome_driver_configuration() -> Options:
        """
        Configures Chrome WebDriver options for Selenium.
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument(
            "--disable-features=IsolateOrigins,site-per-process"
        )
        chrome_options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess"
        )
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return chrome_options

    def _load_cookies(self):
        """
        Pulls active Facebook session directly from Firefox with fixed expiry handling.
        """
        import browser_cookie3
        rprint("[bold yellow]🦊 Pulling session from Firefox...[/bold yellow]")
        
        self._driver.get("https://www.facebook.com/")
        
        try:
            cj = browser_cookie3.firefox(domain_name='facebook.com')
            
            for cookie in cj:
                # Prepare a clean cookie dictionary
                new_cookie = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': cookie.path,
                    'domain': '.facebook.com' # Force the domain to ensure matching
                }
                
                # Fix for the 'expiry' error: 
                # Ensure it's an integer or omit it if it's missing/invalid
                if cookie.expires:
                    try:
                        new_cookie['expiry'] = int(cookie.expires)
                    except (ValueError, TypeError):
                        pass # If it's weird, just let Chrome handle it as a session cookie
                
                try:
                    self._driver.add_cookie(new_cookie)
                except Exception as e:
                    # Log specific failures but keep going for others
                    logs.log_error(f"Failed to add individual cookie {cookie.name}: {e}")
            
            rprint("[bold green]✅ Firefox session injected! Refreshing...[/bold green]")
            self._driver.refresh()
            
        except Exception as e:
            rprint(f"[bold red]❌ Failed to pull Firefox cookies: {e}[/bold red]")
            
            