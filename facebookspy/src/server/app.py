from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from .schemas import (
    PersonListSchema,
    PersonDetailSchema,
)
from ..models import Person
from ..database import get_session, Session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
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
    person_id: int, request: Request, db: Session = Depends(get_session)
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        return {"message": "Person not found"}

    family_members = []
    if person.family_member is not None and isinstance(person.family_member, list):
        family_members = [
            {
                "id": fm.id,
                "full_name": fm.full_name,
                "role": fm.role,
                "url": fm.url,
                "person_id": fm.person_id,
            }
            for fm in person.family_member
        ]

    friends = []
    if person.friends is not None and isinstance(person.friends, list):
        friends = [
            {
                "id": friend.id,
                "full_name": friend.full_name,
                "url": friend.url,
                "person_id": friend.person_id,
            }
            for friend in person.friends
        ]

    images = []
    if person.images is not None and isinstance(person.images, list):
        images = [
            {
                "id": image.id,
                "path": image.path.replace("\\", "/").replace("images/", ""),
                "person_id": image.person_id,
            }
            for image in person.images
        ]

    places = []
    if person.places is not None and isinstance(person.places, list):
        places = [
            {
                "id": place.id,
                "name": place.name,
                "date": place.date,
                "person_id": place.person_id,
            }
            for place in person.places
        ]

    work_and_education = []
    if person.work_and_education is not None and isinstance(
        person.work_and_education, list
    ):
        work_and_education = [
            {"id": we.id, "name": we.name, "person_id": we.person_id}
            for we in person.work_and_education
        ]

    recent_places = []
    if person.recent_places is not None and isinstance(person.recent_places, list):
        recent_places = [
            {
                "id": rp.id,
                "localization": rp.localization,
                "date": rp.date,
                "person_id": rp.person_id,
            }
            for rp in person.recent_places
        ]

    reels = []
    if person.reels is not None and isinstance(person.reels, list):
        reels = [
            {
                "id": reel.id,
                "url": reel.url,
                "person_id": reel.person_id,
                "downloaded": reels.downloaded,
            }
            for reel in person.reels
        ]

    videos = []
    if person.videos is not None and isinstance(person.videos, list):
        videos = [
            {
                "id": video.id,
                "url": video.url,
                "person_id": video.person_id,
                "downloaded": video.downloaded,
            }
            for video in person.videos
        ]

    reviews = []
    if person.reviews is not None and isinstance(person.reviews, list):
        reviews = [
            {
                "id": review.id,
                "review": review.review,
                "company": review.company,
                "person_id": review.person_id,
            }
            for review in person.reviews
        ]

    posts = []
    if person.posts is not None and isinstance(person.posts, list):
        posts = [
            {
                "id": post.id,
                "url": post.url,
                "person_id": post.person_id,
                "content": post.content,
                "number_of_likes": post.number_of_likes,
                "number_of_shares": post.number_of_shares,
                "number_of_comments": post.number_of_comments,
                "scraped": post.scraped,
                "source": post.source,
                "classification": post.classification,
                "score": post.score,
            }
            for post in person.posts
        ]

    likes = []
    if person.likes is not None and isinstance(person.likes, list):
        likes = [
            {"id": like.id, "name": like.name, "person_id": like.person_id}
            for like in person.likes
        ]

    groups = []
    if person.groups is not None and isinstance(person.groups, list):
        groups = [
            {
                "id": group.id,
                "name": group.name,
                "url": group.url,
                "person_id": group.person_id,
            }
            for group in person.groups
        ]

    events = []
    if person.events is not None and isinstance(person.events, list):
        events = [
            {
                "id": event.id,
                "name": event.name,
                "url": event.url,
                "person_id": event.person_id,
            }
            for event in person.events
        ]

    person_data = PersonDetailSchema(
        id=person.id,
        full_name=person.full_name,
        url=person.url,
        facebook_id=person.facebook_id,
        phone_number=person.phone_number,
        email=person.email,
        number_of_friends=person.number_of_friends,
        ai_summary=person.ai_summary,
        family_member=family_members,
        friends=friends,
        images=images,
        places=places,
        work_and_education=work_and_education,
        recent_places=recent_places,
        reels=reels,
        videos=videos,
        reviews=reviews,
        posts=posts,
        likes=likes,
        groups=groups,
        events=events,
    )

    return templates.TemplateResponse(
        "person_detail.html", {"request": request, "person": person_data}
    )
