import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import (
    Person,
    FamilyMember,
    Friends,
    Image,
    Places,
    WorkAndEducation,
    Base,
)

engine = create_engine("sqlite:///database_test.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
