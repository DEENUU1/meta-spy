from pydantic import BaseModel
from typing import Optional


class FriendsSchema(BaseModel):
    full_name: str
    url: Optional[str] = None


class ImageSchema(BaseModel):
    path: str


class PlacesSchema(BaseModel):
    name: str
    date: Optional[str] = None


class WorkAndEducationSchema(BaseModel):
    name: str


class FamilyMemberSchema(BaseModel):
    full_name: str
    role: Optional[str] = None
    url: Optional[str] = None


class PersonSchema(BaseModel):
    full_name: str
    url: Optional[str] = None
    facebook_id: Optional[str] = None

    class Config:
        orm_mode = True
