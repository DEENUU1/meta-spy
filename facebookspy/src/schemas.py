from pydantic import BaseModel

from typing import Optional


class FamilyMemberSchema(BaseModel):
    id: int
    full_name: str
    role: str = None
    url: str = None
    person_id: int

    class Config:
        orm_mode = True


class FriendsSchema(BaseModel):
    id: int
    full_name: str
    url: Optional[str] = None
    person_id: int
    has_multiple_persons: bool

    def __init__(self, *, has_multiple_persons: bool, **data):
        super().__init__(**data)
        self.has_multiple_persons = has_multiple_persons

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    id: int
    path: str
    person_id: int

    class Config:
        orm_mode = True


class PlacesSchema(BaseModel):
    id: int
    name: str
    date: str = None
    person_id: int

    class Config:
        orm_mode = True


class WorkAndEducationSchema(BaseModel):
    id: int
    name: str
    person_id: int

    class Config:
        orm_mode = True


class RecentPlacesSchema(BaseModel):
    id: int
    localization: str
    date: str = None
    person_id: int

    class Config:
        orm_mode = True


class ReelsSchema(BaseModel):
    id: int
    url: str
    person_id: int

    class Config:
        orm_mode = True


class VideosSchema(BaseModel):
    id: int
    url: str
    person_id: int

    class Config:
        orm_mode = True


class ReviewsSchema(BaseModel):
    id: int
    company: str
    review: str
    person_id: int

    class Config:
        orm_mode = True


class PersonSchema(BaseModel):
    id: int
    full_name: str | None
    url: str
    facebook_id: str

    class Config:
        orm_mode = True
