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


def update_crawler_queue_status(crawler_queue_id: int) -> bool:
    """
    Update field 'status' in specified crawlerqueue object

    Args:
        crawler_queue_id (int): CrawlerQueue ID
    """
    session = get_session()
    crawler_queue = session.query(CrawlerQueue).filter_by(id=crawler_queue_id).first()
    if not crawler_queue:
        return False
    crawler_queue.status = 1
    session.commit()
    return True
