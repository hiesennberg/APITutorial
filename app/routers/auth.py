from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import schema
from sqlalchemy.orm import Session

from app import oauth2
from .. import Schema, utils, Database, models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=['authentication'])

@router.post('/login', response_model= Schema.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session=Depends(Database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return { "access_token": access_token, "token_type": "bearer"}
    
    