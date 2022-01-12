from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr
from pydantic.types import conint
from sqlalchemy.sql.expression import true

from app.Database import Base



class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserCreatedResponse(BaseModel):
    email : EmailStr
    id : int
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str





class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    
class PostCreate(PostBase):
    pass

class PostModel(PostBase):
    pass


class PostResponse(BaseModel):
    title: str
    content: str
    published : bool = True
    id : int
    created : datetime
    user_id : int
    owner : UserCreatedResponse
    
    class Config:
        orm_mode =True
       
class PostOut(BaseModel):
    Post : PostResponse
    votes : int
    
    class Config:
        orm_mode = True 
    
class Token(BaseModel):
    access_token : str
    token_type : str
     
class TokenData(BaseModel):
    id : Optional[str]
    
class Vote(BaseModel):
    post_id : int
    dir : bool