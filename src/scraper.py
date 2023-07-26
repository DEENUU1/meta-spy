from selenium.webdriver.chrome.options import Options
from abc import ABC, abstractmethod


class Scraper(ABC):
    """
    Base class for web scrapers.

    This class provides common methods and configurations for web scraping tasks using Selenium.

    Attributes:
        None

    Methods:
        _chrome_driver_configuration() -> Options:
            Configures Chrome WebDriver options for Selenium.

            Returns:
                Options: A configured ChromeOptions instance to be used with Chrome WebDriver.
    """

    @abstractmethod
    def _load_cookies(self) -> None:
        """
        Abstract method to be implemented by subclasses.

        Load cookies with a log in session
        """
        pass

    @staticmethod
    def _chrome_driver_configuration() -> Options:
        """
        Configures Chrome WebDriver options for Selenium.

        This static method creates a set of options that can be passed to the Chrome WebDriver
        when creating an instance of it. These options modify the behavior of the Chrome browser
        during automated testing or scraping.

        Returns:
            Options: A configured ChromeOptions instance to be used with Chrome WebDriver.
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
        return chrome_options
