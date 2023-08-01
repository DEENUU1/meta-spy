from fastapi import FastAPI, Depends
from typing import List, Annotated
from ...schemas import PersonSchema, ReviewsSchema
from ...repository import get_people, get_person_by_facebook_id, get_reviews_list

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/people/", response_model=List[PersonSchema])
async def get_people_list(people: Annotated[List[PersonSchema], Depends(get_people)]):
    """Returns a list of people"""
    return people


@app.get("/people/{facebook_id}", response_model=PersonSchema)
async def get_person_by_facebook_id(
    person: PersonSchema = Depends(get_person_by_facebook_id),
):
    """Returns a person object based on facebook_id"""
    return person


@app.get("/review/{person_id}", response_model=List[ReviewsSchema])
async def get_reviews_by_person_id(
    reviews: List[ReviewsSchema] = Depends(get_reviews_list),
):
    """Returns a list of reviews for specified person object"""
    return reviews
