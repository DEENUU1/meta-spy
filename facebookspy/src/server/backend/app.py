from fastapi import FastAPI
from typing import List
from ...schemas import PersonSchema
from ...repository import (
    get_people,
)

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/people/", response_model=List[PersonSchema])
def get_people_list():
    people = get_people()
    return people
