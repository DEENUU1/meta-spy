from fastapi import FastAPI, Depends
from typing import List, Annotated
from ...schemas import PersonSchema
from ...repository import get_people, get_person

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/people/")
async def get_people_list(people: Annotated[List[PersonSchema], Depends(get_people)]):
    return people


@app.get("/people/{facebook_id}", response_model=PersonSchema)
async def get_person_by_facebook_id(facebook_id: str):
    person = await get_person(facebook_id)
    return person
