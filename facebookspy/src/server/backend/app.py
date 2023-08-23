from fastapi import FastAPI, Depends, HTTPException
from typing import List

from sqlalchemy import or_

from ...schemas import (
    PersonSchema,
    ReviewsSchema,
    VideosSchema,
    ReelsSchema,
    RecentPlacesSchema,
    WorkAndEducationSchema,
    PlacesSchema,
    FriendsSchema,
    ImageSchema,
    FamilyMemberSchema,
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteSchema,
    PostSchema,
    LikeSchema,
    GroupSchema,
    EventSchema,
)
from ...models import (
    Person,
    Videos,
    Reviews,
    Reels,
    RecentPlaces,
    WorkAndEducation,
    Places,
    Friends,
    Image,
    FamilyMember,
    Notes,
    Posts,
    Likes,
    Groups,
    Events,
)

from ...database import Session, get_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from ...config import Config

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/person/", response_model=List[PersonSchema])
async def get_people_list(session: Session = Depends(get_session)):
    """Returns a list of person objects"""
    people = session.query(Person).all()
    if not people:
        raise HTTPException(status_code=404, detail="People not found")
    return people


@app.get("/person/{person_id}", response_model=PersonSchema)
async def get_person_by_facebook_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a person object based on facebook_id"""
    person = session.query(Person).filter_by(id=person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.get("/person/review/{person_id}", response_model=List[ReviewsSchema])
async def get_reviews_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reviews for specified person object"""
    reviews = session.query(Reviews).filter_by(person_id=person_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews


@app.get("/person/video/{person_id}", response_model=List[VideosSchema])
async def get_videos_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of videos for specified person object"""
    videos = session.query(Videos).filter_by(person_id=person_id).all()
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")
    return videos


@app.get("/person/reel/{person_id}", response_model=List[ReelsSchema])
async def get_reels_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reels for specified person object"""
    reels = session.query(Reels).filter_by(person_id=person_id).all()
    if not reels:
        raise HTTPException(status_code=404, detail="Reels not found")
    return reels


@app.get("/person/recent_place/{person_id}", response_model=List[RecentPlacesSchema])
async def get_recent_places_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of recent places for specified person object"""
    recent_places = session.query(RecentPlaces).filter_by(person_id=person_id).all()
    if not recent_places:
        raise HTTPException(status_code=404, detail="Recent Places not found")
    return recent_places


@app.get(
    "/person/work_and_education/{person_id}",
    response_model=List[WorkAndEducationSchema],
)
async def get_work_and_education_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of work and education for specified person object"""
    work_and_education = (
        session.query(WorkAndEducation).filter_by(person_id=person_id).all()
    )
    if not work_and_education:
        raise HTTPException(status_code=404, detail="Work and Education not found")
    return work_and_education


@app.get("/person/place/{person_id}", response_model=List[PlacesSchema])
async def get_places_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of places for specified person object"""
    places = session.query(Places).filter_by(person_id=person_id).all()
    if not places:
        raise HTTPException(status_code=404, detail="Places not found")
    return places


@app.get("/person/friend/{person_id}", response_model=List[FriendsSchema])
async def get_friends_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of friends for specified person object"""
    friends = session.query(Friends).filter_by(person_id=person_id).all()
    if not friends:
        raise HTTPException(status_code=404, detail="Friends not found")
    return friends


@app.get("/person/image/{person_id}", response_model=List[ImageSchema])
async def get_images_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of images for specified person object"""
    images = session.query(Image).filter_by(person_id=person_id).all()
    if not images:
        raise HTTPException(status_code=404, detail="Images not found")
    return images


@app.get("/person/image/{image_id}/view")
async def view_image_by_image_id(
    image_id: int, session: Session = Depends(get_session)
):
    """View an image for the specified image_id"""
    image = session.query(Image).filter_by(id=image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    image_path = Config.DOCKER_IMAGE_PATH / Path(image.path.replace("\\", "/"))
    if not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(image_path, media_type="image/jpeg")


@app.get("/person/family_member/{person_id}", response_model=List[FamilyMemberSchema])
async def get_family_member_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of family members for specified person object"""
    family_members = session.query(FamilyMember).filter_by(person_id=person_id).all()
    if not family_members:
        raise HTTPException(status_code=404, detail="Family Members not found")
    return family_members


@app.post("/person/note/{person_id}", response_model=NoteSchema)
async def create_note_for_person(
    person_id: int, note: NoteCreateSchema, db: Session = Depends(get_session)
):
    """Create note object for specified person"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    db_note = Notes(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.put("/person/note/{person_id}", response_model=NoteSchema)
async def update_note_for_person(
    person_id: int, note: NoteUpdateSchema, db: Session = Depends(get_session)
):
    """Update note object for specified person"""
    db_note = db.query(Notes).filter(Notes.person_id == person_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note


@app.get("/person/note/{person_id}", response_model=NoteSchema)
async def get_note_for_person(person_id: int, db: Session = Depends(get_session)):
    """Return note object for specified person"""
    db_note = db.query(Notes).filter(Notes.person_id == person_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@app.get("/note/", response_model=List[NoteSchema])
async def get_all_notes(db: Session = Depends(get_session)):
    """Return a list of notes"""
    db_note = db.query(Notes).all()
    if not db_note:
        raise HTTPException(status_code=404, detail="Notes not found")
    return db_note


@app.get("/friends/search/", response_model=List[FriendsSchema])
async def search_friends(search_term: str, db: Session = Depends(get_session)):
    """Search Friend objects"""
    friends = (
        db.query(Friends).filter(Friends.full_name.ilike(f"%{search_term}%")).all()
    )
    if not friends:
        raise HTTPException(status_code=404, detail="Friends not found")
    return friends


@app.get("/person/search/", response_model=List[PersonSchema])
async def search_person(search_term: str, db: Session = Depends(get_session)):
    """Search Person objects"""
    person = (
        db.query(Person)
        .filter(
            or_(
                Person.full_name.ilike(f"%{search_term}%"),
                Person.facebook_id.ilike(f"%{search_term}%"),
            )
        )
        .all()
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.get("/person/post/{person_id}", response_model=List[PostSchema])
async def get_posts_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of posts for specified person object"""
    posts = session.query(Posts).filter_by(person_id=person_id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Family Members not found")
    return posts


@app.get("/person/like/{person_id}", response_model=List[LikeSchema])
async def get_likes_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of likes for specified person object"""
    likes = session.query(Likes).filter_by(person_id=person_id).all()
    if not likes:
        raise HTTPException(status_code=404, detail="Likes not found")
    return likes


@app.get("/person/group/{person_id}", response_model=List[GroupSchema])
async def get_groups_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of groups for specified person object"""
    groups = session.query(Groups).filter_by(person_id=person_id).all()
    if not groups:
        raise HTTPException(status_code=404, detail="Groups not found")
    return groups


@app.get("/person/event/{person_id}", response_model=List[EventSchema])
async def get_events_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of events for specified person object"""
    events = session.query(Events).filter_by(person_id=person_id).all()
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")
    return events
