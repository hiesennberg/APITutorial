from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:power123#@localhost/FastAPI'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# try:
#     conn = psycopg2.connect(host='localhost', database='FastAPI',
#                             user='postgres', password='power123#', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("DB Connection Sucessfull")

# except Exception as e:
#     print(f"Connecting to DB failed. \n {e}")
