import json

import pytest
from app import Schema
from typing import List

def test_all_posts(authorized_client, create_posts):
    res = authorized_client.get('/posts/')
    def validate(post):
        return Schema.PostOut(**post)
    
    posts_mapped = list(map(validate,res.json()))
    
    #print(posts_mapped)
    assert len(res.json()) == len(create_posts)
    assert res.status_code == 200
    
    
def test_Unauthorized_get_all_post(client,create_posts):
    res = client.get('/posts/')
    assert res.status_code == 401
    
def test_Unauthorized_get_one_post(client,create_posts):
    id = create_posts[0].id
    res = client.get(f'/posts/{id}')
    assert res.status_code == 401
    
def test_get_nonExisting_post(authorized_client,create_posts):
    res = authorized_client.get('/posts/999')
    assert res.status_code == 404
    
def test_get_one_post(authorized_client,create_posts):
    res = authorized_client.get(f'/posts/{create_posts[0].id}')
    post_res = Schema.PostOut(**res.json())
    
    assert post_res.Post.id == create_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title,content,published",[
    ("Title1","Content 1","true"),
    ("Pizza","Hut","false"),
    ("travel Guide","For Beach Only","true")
])
def test_create_post(authorized_client,test_user,create_posts,title,content,published):
    res = authorized_client.post('/posts',json = {"title":title,"content":content,"published":published})
    
    created_post = Schema.PostResponse(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.user_id == test_user['id']
    
    
def test_create_default_published_post(authorized_client,test_user,create_posts):
    res = authorized_client.post('/posts',json = {"title":"title1","content":"Content New"})
    
    created_post = Schema.PostResponse(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == "title1"
    assert created_post.content == "Content New"
    assert created_post.user_id == test_user['id']
    assert bool(created_post.published) == True
    
    
def test_create_post_unauthorized_user(client,test_user,create_posts):
    res = client.post('/posts',json = {"title":"title1","content":"Content New"})
        
    assert res.status_code == 401
    
    
def test_unauthorized_user_delete_post(client,test_user,create_posts):
    
    res =client.delete(f'/posts/{create_posts[0].id}')
    
    assert res.status_code == 401
    
def test_delete_post_sucess(authorized_client,test_user,create_posts):
    
    res = authorized_client.delete(f'/posts/{create_posts[0].id}')
    
    assert res.status_code == 204
    

def test_delete_post_nonexist(authorized_client,test_user,create_posts):
    
    res = authorized_client.delete(f'/posts/9899')
         
    assert res.status_code == 404
    

def test_delete_post_nonexist(authorized_client,test_user,create_posts):
    
    res = authorized_client.delete(f'/posts/{create_posts[3].id}')
         
    assert res.status_code == 403
    
def test_update_post(authorized_client,test_user,create_posts):
    
    data = {
        "title" : "Updated Title",
        "content" : "Updated Content",
        "id" : create_posts[0].id
    }
    res = authorized_client.put(f'/posts/{create_posts[0].id}',json=data)
    updated_post = Schema.PostModel(**res.json())
    
    assert res.status_code == 202
    assert updated_post.title == data['title']
    
def test_update_other_user_post(authorized_client,test_user,create_posts):
    
    
    data = {
        "title" : "Updated Title",
        "content" : "Updated Content",
        "id" : create_posts[0].id
    }
    res = authorized_client.put(f'/posts/{create_posts[3].id}',json=data)
    #updated_post = Schema.PostModel(**res.json())
    
    assert res.status_code == 403
    #assert updated_post.title == data['title']
    
def test_unauthorized_user_update_post(client,test_user,create_posts):
    
    
    data = {
        "title" : "Updated Title",
        "content" : "Updated Content",
        "id" : create_posts[0].id
    }
    
    res =client.put(f'/posts/{create_posts[0].id}',json=data)
    
    assert res.status_code == 401


def test_update_post_nonexist(authorized_client,test_user,create_posts):
    
    
    data = {
        "title" : "Updated Title",
        "content" : "Updated Content",
        "id" : create_posts[0].id
    }
    
    res = authorized_client.put(f'/posts/80000',json=data)
    
    assert res.status_code == 404
