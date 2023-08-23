from pydantic import BaseModel

from typing import Optional
from .models import PostSource


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
    phone_number: str | None
    email: str | None

    class Config:
        orm_mode = True


class NoteBaseSchema(BaseModel):
    content: Optional[str] = None


class NoteCreateSchema(NoteBaseSchema):
    person_id: int


class NoteUpdateSchema(NoteBaseSchema):
    pass


class NoteSchema(NoteBaseSchema):
    id: int
    person_id: int

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: int
    url: str
    person_id: int
    content: Optional[str]
    number_of_likes: Optional[int]
    number_of_shares: Optional[int]
    number_of_comments: Optional[int]
    scraped: bool
    source: PostSource

    class Config:
        orm_mode = True


class LikeSchema(BaseModel):
    id: int
    person_id: int
    name: str

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    id: int
    person_id: int
    name: str
    url: str | None

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    id: int
    person_id: int
    name: str
    url: str | None

    class Config:
        orm_mode = True
