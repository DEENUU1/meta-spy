from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from .schemas import PersonSchema
from ..models import Person
from sqlalchemy import select
from ..database import get_session, Session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/person/", response_class=HTMLResponse)
async def person(request: Request, db: Session = Depends(get_session)):
    persons = db.query(Person).all()

    person_schemas = [
        PersonSchema(
            id=person.id,
            full_name=person.full_name,
            url=person.url,
            facebook_id=person.facebook_id,
        )
        for person in persons
    ]

    return templates.TemplateResponse(
        "person.html", {"request": request, "persons": person_schemas}
    )


@app.get("/person/{person_id}", response_class=HTMLResponse)
async def person_detail(request: Request, person_id: int):
    pass
