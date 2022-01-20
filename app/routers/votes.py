
from app import oauth2
from .. import models, Schema, utils, oauth2
from ..Database import *
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List


router = APIRouter(prefix ="/vote",tags=['votes'])


@router.get("/vote")
def get_votes():
    pass


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: Schema.Vote,db: Session=Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    
    v = {}
    v['post_id'] = vote.post_id
    v['user_id'] = user_id.id
    v = models.Votes(**v)
    if vote.dir:
        try:
            db.add(v)
            db.commit()
            db.refresh(v)
            return(v)

        except Exception as e:
            #print(dir(e))
            #reason = e.reason
            #print(reason)

            if "already exists" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Already voted")
            
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    else:

        votequery = db.query(models.Votes).filter(
            models.Votes.user_id == user_id.id, models.Votes.post_id == vote.post_id)
        
        vote = votequery.first()
        
        if vote == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No vote exists to remove")
        else:
            votequery.delete()
            db.commit()
            return {"message":"vote removed"}
#ll