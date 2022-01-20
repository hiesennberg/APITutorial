import json
from sqlalchemy import null
from app.Database import get_db,Base
from app.main import app
from app import Schema
import pytest

from jose import jwt
from app.config import settings



def test_root(client):
    res = client.get("/")
    #print(res.json().get("message"))
    
    assert res.status_code == 200
    
def test_user_creation(client):
    res = client.post('/users/',json={"email":"Hello123@gmail.com","password":"password123"})
    #print(res.json())
    new_user = Schema.UserCreatedResponse(**(res.json()))
    assert new_user.email == "Hello123@gmail.com"
    assert res.status_code == 201
    
def test_user_loging(test_user,client):
    res = client.post('/login',data={"username":test_user['email'],"password":test_user['password']})
    #print(res.json())
    login_cred = Schema.Token(**(res.json()))
    payload = jwt.decode(login_cred.access_token,settings.secret_key,algorithms = [settings.algorithm])
    #print(login_cred.access_token)
    id =payload.get("user_id")
    assert res.status_code == 200
    assert login_cred.access_token != null
    assert test_user['id'] == id
    assert login_cred.token_type == "bearer"
    

@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@example.com','password123',403),
    ('raainishant@example.com','wrongpassword',403),
    ('hjkj','bajojam',403),
    (None,'password123',422),
    ('raainishant@example.com',None,422)
])
def incorrect_user_login(test_user,client,email,password,status_code):
    res = client.post('/login',data={"username":email,"password":password})
    
    assert res.status_code==status_code
    assert res.json().get("detail") == "Invalid Credentials"
    
    
