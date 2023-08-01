from fastapi import FastAPI, Depends, HTTPException
from typing import List
from ...schemas import PersonSchema, ReviewsSchema
from ...models import Person
from ...database import Session, get_session

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/person/", response_model=List[PersonSchema])
async def get_people_list(session: Session = Depends(get_session)):
    """Returns a list of person objects"""
    people = session.query(Person).all()
    return people


@app.get("/person/{facebook_id}", response_model=PersonSchema)
async def get_person_by_facebook_id(
    facebook_id: str, session: Session = Depends(get_session)
):
    """Returns a person object based on facebook_id"""
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.get("/review/{person_id}", response_model=List[ReviewsSchema])
async def get_reviews_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reviews for specified person object"""
    reviews = session.query(ReviewsSchema).filter_by(person_id=person_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews
