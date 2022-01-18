from operator import imod
from fastapi.testclient import TestClient
from itsdangerous import json
from sqlalchemy import schema
from app.Database import get_db,Base
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest
from alembic import command
from app.oauth2 import create_access_token
from app import models




SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)

#dependency










#client = TestClient(app)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    #run some code before test runs
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
        
    yield TestClient(app)
    #run some code after test runs
    

@pytest.fixture
def test_user2(client):
    user_data =  {"email":"raainishant2@example.com",
                  "password":"password123"}
    res = client.post('/users/',json=user_data)
    assert res.status_code == 201
    data = res.json()
    data['password'] = user_data['password']
    return data





@pytest.fixture
def test_user(client):
    user_data =  {"email":"raainishant@example.com",
                  "password":"password123"}
    res = client.post('/users/',json=user_data)
    assert res.status_code == 201
    data = res.json()
    data['password'] = user_data['password']
    return data


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})
    

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization" : f"bearer {token}"
    }
    return client


@pytest.fixture
def create_posts(test_user,session,test_user2):
    data = [
        {"title":"title_1","content":"content_1","user_id":test_user['id']},
        {"title":"title_2","content":"content_2","user_id":test_user['id']},
        {"title":"title_3","content":"content_3","user_id":test_user['id']},
        {"title":"title_3","content":"content_3","user_id":test_user2['id']}
    ]
    
    session.add_all([models.Post(**x) for x in data])
    session.commit()
    return session.query(models.Post).all()