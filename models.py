from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Post(Base):
    _tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content= Column(String(255))
    user_id = Column(Integer)
    