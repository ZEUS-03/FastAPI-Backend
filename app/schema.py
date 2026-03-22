from enum import Enum
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}

class Login(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: User
    model_config = {
        "from_attributes": True
    }

class PostOut(PostBase):
    Post: Post
    votes: int

    model_config = {
        "from_attributes": True
    }

class TokenData(BaseModel):
    id: Optional[int]

class Token(BaseModel):
    access_token: str
    token_type: str

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

class GetVote(BaseModel):
    post_id: int