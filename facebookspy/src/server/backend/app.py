from fastapi import FastAPI, Depends, HTTPException
from typing import List

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
)
from ...database import Session, get_session

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/person/", response_model=List[PersonSchema])
async def get_people_list(session: Session = Depends(get_session)):
    """Returns a list of person objects"""
    people = session.query(Person).all()
    if not people:
        raise HTTPException(status_code=404, detail="People not found")
    return people


@app.get("/person/{facebook_id}", response_model=PersonSchema)
async def get_person_by_facebook_id(
    facebook_id: str, session: Session = Depends(get_session)
):
    """Returns a person object based on facebook_id"""
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.get("/review/{person_id}", response_model=List[ReviewsSchema])
async def get_reviews_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reviews for specified person object"""
    reviews = session.query(Reviews).filter_by(person_id=person_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews


@app.get("/video/{person_id}", response_model=List[VideosSchema])
async def get_videos_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of videos for specified person object"""
    videos = session.query(Videos).filter_by(person_id=person_id).all()
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")
    return videos


@app.get("/reels/{person_id}", response_model=List[ReelsSchema])
async def get_reels_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of reels for specified person object"""
    reels = session.query(Reels).filter_by(person_id=person_id).all()
    if not reels:
        raise HTTPException(status_code=404, detail="Reels not found")
    return reels


@app.get("/recent_places/{person_id}", response_model=List[RecentPlacesSchema])
async def get_recent_places_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Returns a list of recent places for specified person object"""
    recent_places = session.query(RecentPlaces).filter_by(person_id=person_id).all()
    if not recent_places:
        raise HTTPException(status_code=404, detail="Recent Places not found")
    return recent_places


@app.get("/work_and_education/{person_id}", response_model=List[WorkAndEducationSchema])
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


@app.get("/places/{person_id}", response_model=List[PlacesSchema])
async def get_places_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of places for specified person object"""
    places = session.query(Places).filter_by(person_id=person_id).all()
    if not places:
        raise HTTPException(status_code=404, detail="Places not found")
    return places


@app.get("/friends/{person_id}", response_model=List[FriendsSchema])
async def get_friends_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of friends for specified person object"""
    friends = session.query(Friends).filter_by(person_id=person_id).all()
    if not friends:
        raise HTTPException(status_code=404, detail="Friends not found")
    return friends


@app.get("/image/{person_id}", response_model=List[ImageSchema])
async def get_images_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of images for specified person object"""
    images = session.query(Image).filter_by(person_id=person_id).all()
    if not images:
        raise HTTPException(status_code=404, detail="Images not found")
    return images


@app.get("/image/{image_id}", response_model=ImageSchema)
async def get_image_by_image_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of images for specified person object"""
    images = session.query(Image).filter_by(person_id=person_id).all()
    if not images:
        raise HTTPException(status_code=404, detail="Images not found")
    return images


@app.get("/family_member/{person_id}", response_model=List[FamilyMemberSchema])
async def get_family_member_by_person_id(
    person_id: int, session: Session = Depends(get_session)
):
    """Return a list of family members for specified person object"""
    family_members = session.query(FamilyMember).filter_by(person_id=person_id).all()
    if not family_members:
        raise HTTPException(status_code=404, detail="Family Members not found")
    return family_members
