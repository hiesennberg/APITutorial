from app import oauth2
from .. import models, Schema, utils, oauth2
from ..Database import *
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func

router = APIRouter( tags = ['posts'])

@router.get("/posts", response_model=List[Schema.PostOut])
async def get_post(db: Session = Depends(get_db), limit : int = 10, skip : int = 0, search : Optional[str] = "",user_id: int = Depends(oauth2.get_current_user)):
    
    
    posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    #print(posts)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    #print(limit)

    # cursor.execute("Select * from public.posts;")
    # posts = cursor.fetchall()
    # print(posts)
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= Schema.PostResponse)
def create_post(new_post: Schema.PostModel, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""insert into public.posts (title, content, is_published) values (%s,%s,%s) returning *;""",
    #                (new_post.title,new_post.content,new_post.published))

    # return_post = cursor.fetchone()
    print(user_id)
    
    Post_with_ID = new_post.dict()
    Post_with_ID['user_id'] = user_id.id
    
    ret_post = models.Post(**Post_with_ID)

    db.add(ret_post)
    db.commit()
    db.refresh(ret_post)

    return ret_post


@router.get('/posts/{id}', response_model = Schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""select * from public.posts where id = (%s);""",(id,))
    # p = cursor.fetchone()
    p = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id {id} not found'}

    return p


@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""delete from public.posts where id = %s returning *""",(id,))
    # d = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    post_data = post.first()
    


    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
        
    elif post_data.user_id != int(user_id.id):
        raise(HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='You can delete only your posts'))       
        

    else:
        post.delete(synchronize_session=False)

    db.commit()


    return post







@router.put('/posts/{id}', status_code = status.HTTP_202_ACCEPTED, response_model = Schema.PostResponse)
def updatePost(id: int, post: Schema.PostModel, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""update public.posts set title=%s ,content = %s, is_published = %s where id = %s returning * ;""",
    #                (post.title,post.content,post.published,id))
    # p = cursor.fetchone()
    # conn.commit()

    post_Query = db.query(models.Post).filter(models.Post.id == id)

    p = post_Query.first()

    if p == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
        
    elif p.user_id != int(user_id.id):
        raise(HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='You can Update only your posts'))       
    

    else:
        post_Query.update(post.dict(), synchronize_session=False)
        db.commit()

    return post_Query.first()
