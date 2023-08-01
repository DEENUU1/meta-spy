from fastapi import FastAPI, Depends
from typing import List, Annotated
from ...schemas import PersonSchema
from ...repository import (
    get_people,
)

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/people/")
def get_people_list(people: Annotated[List[PersonSchema], Depends(get_people)]):
    return people
