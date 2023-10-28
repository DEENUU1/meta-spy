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
    crawler_queue.status = True
    session.commit()
    return True


def get_crawler_queues_status_false() -> List[CrawlerQueue]:
    """
    Get crawlerqueue objects with status = True
    """
    session = get_session()
    return session.query(CrawlerQueue).filter_by(status=False).all()


def delete_all() -> bool:
    """
    Delete all objects from CrawlerQueue
    """
    session = get_session()
    session.query(CrawlerQueue).delete()
    session.commit()

    return True if session.query(CrawlerQueue).count() == 0 else False


def delete_crawler_queue(crawler_queue_id: int) -> bool:
    """
    Delete specified crawlerqueue object
    """
    session = get_session()
    crawler_queue = session.query(CrawlerQueue).filter_by(id=crawler_queue_id).first()
    if not crawler_queue:
        return False
    session.delete(crawler_queue)
    session.commit()
    return True


def crawler_queue_exists(url: str) -> bool:
    """
    Check if crawlerqueue object with specified url exists
    """
    session = get_session()
    return True if session.query(CrawlerQueue).filter_by(url=url).first() else False
