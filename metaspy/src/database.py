from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

db_path = "sqlite:///database.db"

engine = create_engine(db_path, max_overflow=-1)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
