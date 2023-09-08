from ..models import CrawlerQueue
from ..database import get_session
from typing import List


def create_crawler_queue(url: str) -> CrawlerQueue:
    """
    Create a CrawlerQueue object

    Args:
        url (str): URL to crawl

    Returns:
        CrawlerQueue: CrawlerQueue object
    """
    session = get_session()
    crawler_queue = CrawlerQueue(url=url)
    session.add(crawler_queue)
    session.commit()
    return crawler_queue
