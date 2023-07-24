from typing import Type

from sqlalchemy.orm import Session
from models import Queue


def create_queue(db: Session, url: str) -> Queue:
    """Create queue object"""
    db_item = Queue(url=url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_queue_status_to_true(db: Session, queue_id: int) -> Type[Queue]:
    """Update queue status to True"""
    db_item = db.query(Queue).filter(Queue.id == queue_id).first()
    if db_item:
        db_item.status = True
        db.commit()
        db.refresh(db_item)
    else:
        raise Exception("Queue not found")
    return db_item
