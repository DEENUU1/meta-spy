from time import sleep

from ..config import Config
from ..logs import Logs

logs = Logs()


def scroll_page(driver) -> None:
    """
    Scrolls the page to load more data from a website
    """
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        consecutive_scrolls = 0

        while consecutive_scrolls < Config.MAX_CONSECUTIVE_SCROLLS:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(Config.SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                consecutive_scrolls += 1
            else:
                consecutive_scrolls = 0

            last_height = new_height
    except Exception as e:
        logs.log_error(f"Error occurred while scrolling: {e}")


def scroll_page_callback(driver, callback) -> None:
    """
    Scrolls the page to load more data from a website
    """
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        consecutive_scrolls = 0

        while consecutive_scrolls < Config.MAX_CONSECUTIVE_SCROLLS:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(Config.SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                consecutive_scrolls += 1
            else:
                consecutive_scrolls = 0

            last_height = new_height

            callback(driver)

    except Exception as e:
        logs.log_error(f"Error occurred while scrolling: {e}")
