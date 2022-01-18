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
    
