from sqlalchemy.engine import base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .Database import Base
from sqlalchemy import column, Integer, String, Boolean
from sqlalchemy.sql.expression import text

    
class User(Base):
    __tablename__ = "users"
    
    email = Column(String, nullable=False, unique= True)
    password = Column(String,nullable=False)
    id = Column(Integer, primary_key = True, nullable= False)
    created = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    phone_number = Column(String)



class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer,primary_key=True, nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    created = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id",ondelete= "CASCADE"),nullable=False)
    owner = relationship("User")
    
class Votes(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=true)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=true)
    
    
