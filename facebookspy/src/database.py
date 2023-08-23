import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

docker_container = os.environ.get("DOCKER_CONTAINER")

if docker_container == "true":
    db_path = "sqlite:////app/facebookspy/database.db"
else:
    db_path = "sqlite:///database.db"

engine = create_engine(db_path, max_overflow=-1)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
