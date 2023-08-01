from fastapi import FastAPI, Depends
from typing import List, Annotated
from ...schemas import PersonSchema, ReviewsSchema
from ...repository import get_people, get_person_by_facebook_id, get_reviews_list

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/people/")
async def get_people_list(people: Annotated[List[PersonSchema], Depends(get_people)]):
    return people


@app.get("/people/{facebook_id}", response_model=PersonSchema)
async def get_person_by_facebook_id(facebook_id: str):
    person = await get_person_by_facebook_id(facebook_id)
    return person


@app.get("/review/{person_id}", response_model=List[ReviewsSchema])
async def get_reviews_by_person_id(person_id: int):
    reviews = await get_reviews_list(person_id)
    return reviews
