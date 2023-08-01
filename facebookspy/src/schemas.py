from pydantic import BaseModel


class PersonSchema(BaseModel):
    id: int
    full_name: str
    url: str
    facebook_id: str

    class Config:
        orm_mode = True
