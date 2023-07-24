from sqlalchemy.orm import Session
from models import Queue


def create_queue(db: Session, url: str) -> Queue:
    """Create queue object"""
    db_item = Queue(url=url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
