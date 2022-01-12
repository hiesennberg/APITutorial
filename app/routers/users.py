from .. import models, Schema, utils
from fastapi import FastAPI, Response, routing, status, HTTPException , APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from ..Database import *




 # User Login and Signup Section

router = APIRouter( prefix= "/users", tags=['users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Schema.UserCreatedResponse)
def create_user(user: Schema.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password
    user.password = utils.do_hash(user.password)

    user_post = models.User(**user.dict())

    db.add(user_post)
    db.commit()
    x= {}
    db.refresh(user_post)
    
    return user_post

@router.get("/{id}", response_model = Schema.UserCreatedResponse)
def get_user(id : int, db: Session = Depends(get_db)):
    
    user_info = db.query(models.User).filter(models.User.id == id).first()
    
    return user_info
    