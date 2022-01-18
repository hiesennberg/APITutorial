import pytest
from app import models

@pytest.fixture
def test_vote(create_posts,session, test_user):
    vote = models.Votes(post_id=create_posts[3].id,user_id=test_user['id'])
    session.add(vote)
    session.commit()

def test_vote_post(authorized_client,test_user,create_posts):
    
    res = authorized_client.post("/vote/",json={"post_id":create_posts[0].id,"dir":1 })
    
    res.status_code == 201
    
def test_already_liked_post(authorized_client,test_user,create_posts,test_vote):
    res = authorized_client.post("/vote/", json = {"post_id": create_posts[3].id, "dir": 1})
     
    assert res.status_code == 409
    
def test_delete_vote(authorized_client,create_posts,test_vote):
    res = authorized_client.post("/vote/", json = {"post_id": create_posts[3].id, "dir": 0})
     
    assert res.status_code == 201
    assert res.json().get("message") == "vote removed"
    
    

def test_delete_vote_nonexist(authorized_client,create_posts):
    res = authorized_client.post("/vote/", json = {"post_id": create_posts[3].id, "dir": 0})
     
    assert res.status_code == 404
   

def test_vote_nonexisting_post(authorized_client,test_user,create_posts):
    
    res = authorized_client.post("/vote/",json={"post_id":9999,"dir":1 })
    
    res.status_code == 404
    
    

def test_vote_post_unauthorized(client,test_user,create_posts):
    
    res = client.post("/vote/",json={"post_id":create_posts[2].id,"dir":1 })
    
    res.status_code == 401