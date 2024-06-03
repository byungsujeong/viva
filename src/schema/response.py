from datetime import datetime

from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        orm_mode = True


class JWTResponse(BaseModel):
    access_token: str
    refresh_token: str


class BulletinBoardSchema(BaseModel):
    title: str
    contents: str
    hits: int
    user_id: int

    class Config:
        orm_mode = True


class BulletinBoardListSchema(BaseModel):
    bbs: List[BulletinBoardSchema]


class UsernameResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class BulletinBoardListResponse(BaseModel):
    id: int
    title: str
    hits: int
    user: UsernameResponse

    class Config:
        orm_mode = True
    

class BulletinBoardDetailResponse(BaseModel):
    id: int
    title: str
    contents: str
    hits: int
    created_at: datetime
    updated_at: datetime | str
    user: UsernameResponse

    class Config:
        orm_mode = True
