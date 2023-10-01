from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from .schemas import PersonListSchema, PersonDetailSchema
from ..models import Person
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
        PersonListSchema(
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
async def person_detail(
    request: Request, db: Session = Depends(get_session), person_id: int = 1
):
    person = db.query(Person).filter(Person.id == person_id).first()

    person_data = PersonDetailSchema(
        id=person.id,
        full_name=person.full_name,
        url=person.url,
        facebook_id=person.facebook_id,
        phone_number=person.phone_number,
        email=person.email,
        number_of_friends=person.number_of_friends,
        ai_summary=person.ai_summary,
    )

    return templates.TemplateResponse(
        "person_detail.html", {"request": request, "person": person_data}
    )
    pass
