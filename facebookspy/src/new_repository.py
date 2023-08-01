from .database import Session
from .models import Person
from typing import List


def get_persons() -> List[Person]:
    session = Session()
    persons = session.query(Person).all()
    session.close()
    return persons
