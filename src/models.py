from sqlalchemy import Column, String
from sqlalchemy import Boolean, Integer, DateTime
from database import Base
import datetime
from pydantic import BaseModel


class Queue(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    done = Column(Boolean, default=False)


class QueueBase(BaseModel):
    url: str
    datetime: datetime.datetime
    done: bool

    class Config:
        orm_mode = True
