
from fastapi import FastAPI
from starlette.middleware.cors import ALL_METHODS
from . import models
from .Database import engine
#from .utils import *
from .routers import post,users,auth,votes
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


my_posts = [{"title": "First Post", "content": "explosive", "id": 1}, {
    "title": "Favourite Food", "content": "burgen & Pizza", "id": 2}]




app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message": "Heroku deployment via git sucessfull"}



