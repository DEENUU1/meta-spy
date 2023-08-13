from fastapi import FastAPI, Depends, HTTPException, status
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
)
from ...database import Session, get_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from ...config import Config
from fastapi.responses import JSONResponse

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


@app.post("/person/", response_model=PersonSchema)
async def create_person(
    facebook_id: str, person: PersonSchema, db: Session = Depends(get_session)
):
    """Create a Person object"""
    person_object = db.query(Person).filter(Person.facebook_id == facebook_id).first()
    if person_object:
        raise HTTPException(status_code=404, detail="Person already exist")
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Person object created"
    )


@app.delete("/person/", response_model=PersonSchema)
async def delete_person(person_id: int, db: Session = Depends(get_session)):
    """Delete a Person object"""
    person_object = db.query(Person).filter(Person.id == person_id).first()
    if not person_object:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(person_object)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"Person {person_id} deleted"
    )


@app.get("/person/review/{person_id}", response_model=List[ReviewsSchema])
async def get_reviews_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reviews for specified person object"""
    reviews = session.query(Reviews).filter_by(person_id=person_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews


@app.post("/review/", response_model=ReviewsSchema)
async def create_review(
    person_id: int, review: ReviewsSchema, db: Session = Depends(get_session)
):
    """Create a review object"""
    person_object = db.query(Person).filter(Person.id == person_id).first()
    if not person_object:
        raise HTTPException(status_code=404, detail="Person object not found")

    db_review = Reviews(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Review object created"
    )


@app.delete("/review/", response_model=ReviewsSchema)
async def delete_review(review_id: int, db: Session = Depends(get_session)):
    """Delete a review object"""
    review_object = db.query(Reviews).filter(Reviews.id == review_id).first()
    if not review_object:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review_object)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"Review {review_id} deleted"
    )


@app.get("/person/video/{person_id}", response_model=List[VideosSchema])
async def get_videos_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of videos for specified person object"""
    videos = session.query(Videos).filter_by(person_id=person_id).all()
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")
    return videos


@app.post("/video/", status_code=status.HTTP_201_CREATED)
async def create_video(
    person_id: int, video: VideosSchema, db: Session = Depends(get_session)
):
    """Create a video object for the specified person ID"""
    person_object = db.query(Person).filter(Person.id == person_id).first()
    if not person_object:
        raise HTTPException(status_code=404, detail="Person not found")

    db_video = Videos(**video.dict(), person_id=person_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)


@app.delete("/video/", status_code=status.HTTP_200_OK)
async def delete_video(video_id: int, db: Session = Depends(get_session)):
    """Delete a video object by ID"""
    video_object = db.query(Videos).filter(Videos.id == video_id).first()
    if not video_object:
        raise HTTPException(status_code=404, detail="Video not found")

    db.delete(video_object)
    db.commit()


@app.get("/person/reel/{person_id}", response_model=List[ReelsSchema])
async def get_reels_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reels for specified person object"""
    reels = session.query(Reels).filter_by(person_id=person_id).all()
    if not reels:
        raise HTTPException(status_code=404, detail="Reels not found")
    return reels


@app.post("/reel/", status_code=status.HTTP_201_CREATED)
async def create_reel(
    person_id: int, reel: ReelsSchema, db: Session = Depends(get_session)
):
    """Create a reel object for the specified person ID"""
    person_object = db.query(Person).filter(Person.id == person_id).first()
    if not person_object:
        raise HTTPException(status_code=404, detail="Person not found")

    db_reel = Reels(**reel.dict(), person_id=person_id)
    db.add(db_reel)
    db.commit()
    db.refresh(db_reel)


@app.delete("/reel/", status_code=status.HTTP_200_OK)
async def delete_reel(reel_id: int, db: Session = Depends(get_session)):
    """Delete a reel object by ID"""
    reel_object = db.query(Reels).filter(Reels.id == reel_id).first()
    if not reel_object:
        raise HTTPException(status_code=404, detail="Reel not found")

    db.delete(reel_object)
    db.commit()


@app.get("/person/recent_place/{person_id}", response_model=List[RecentPlacesSchema])
async def get_recent_places_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of recent places for specified person object"""
    recent_places = session.query(RecentPlaces).filter_by(person_id=person_id).all()
    if not recent_places:
        raise HTTPException(status_code=404, detail="Recent Places not found")
    return recent_places


@app.post("/recent_place/", status_code=status.HTTP_201_CREATED)
async def create_recent_place(
    person_id: int, recent_place: RecentPlacesSchema, db: Session = Depends(get_session)
):
    """Create a recent place object for the specified person ID"""
    person_object = db.query(Person).filter(Person.id == person_id).first()
    if not person_object:
        raise HTTPException(status_code=404, detail="Person not found")

    db_recent_place = RecentPlaces(**recent_place.dict(), person_id=person_id)
    db.add(db_recent_place)
    db.commit()
    db.refresh(db_recent_place)


@app.delete("/recent_place/", status_code=status.HTTP_200_OK)
async def delete_recent_place(recent_place_id: int, db: Session = Depends(get_session)):
    """Delete a recent place object by ID"""
    recent_place_object = (
        db.query(RecentPlaces).filter(RecentPlaces.id == recent_place_id).first()
    )
    if not recent_place_object:
        raise HTTPException(status_code=404, detail="Recent Place not found")

    db.delete(recent_place_object)
    db.commit()


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


@app.post("/work_and_education/", status_code=status.HTTP_201_CREATED)
async def create_work_and_education(
    person_id: int,
    work_education: WorkAndEducationSchema,
    db: Session = Depends(get_session),
):
    """Create a work and education object for the specified person ID"""
    person_object = db.query(Person).filter(Person.id == person_id).first()
    if not person_object:
        raise HTTPException(status_code=404, detail="Person not found")

    db_work_education = WorkAndEducation(**work_education.dict(), person_id=person_id)
    db.add(db_work_education)
    db.commit()
    db.refresh(db_work_education)


@app.delete("/work_and_education/", status_code=status.HTTP_200_OK)
async def delete_work_and_education(
    work_education_id: int, db: Session = Depends(get_session)
):
    """Delete a work and education object by ID"""
    work_education_object = (
        db.query(WorkAndEducation)
        .filter(WorkAndEducation.id == work_education_id)
        .first()
    )
    if not work_education_object:
        raise HTTPException(status_code=404, detail="Work and Education not found")

    db.delete(work_education_object)
    db.commit()


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
def create_note_for_person(
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
def update_note_for_person(
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
def get_note_for_person(person_id: int, db: Session = Depends(get_session)):
    """Return note object for specified person"""
    db_note = db.query(Notes).filter(Notes.person_id == person_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@app.get("/note/", response_model=List[NoteSchema])
def get_all_notes(db: Session = Depends(get_session)):
    """Return a list of notes"""
    db_note = db.query(Notes).all()
    if not db_note:
        raise HTTPException(status_code=404, detail="Notes not found")
    return db_note


@app.get("/friends/search/", response_model=List[FriendsSchema])
def search_friends(search_term: str, db: Session = Depends(get_session)):
    """Search Friend objects"""
    friends = (
        db.query(Friends).filter(Friends.full_name.ilike(f"%{search_term}%")).all()
    )
    if not friends:
        raise HTTPException(status_code=404, detail="Friends not found")
    return friends


@app.get("/person/search/", response_model=List[PersonSchema])
def search_person(search_term: str, db: Session = Depends(get_session)):
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
