from pydantic import BaseModel


class UserBase(BaseModel):
    id: str
    email: str
    hashed_password: str


class UserCreate(UserBase):
    pass
