from .db import Base
from sqlalchemy import Column, Integer, String, Text

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index = True)
    email = Column(String, unique=True, index =True)
    hashed_password = Column(String)
    
    
class Project(Base):
    __tablename__ ="projects"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    project_link = Column(String)
    
    
class Blog(Base):
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    author = Column(String)
    published = Column(Integer)
    
class Contact_Info(Base):
    __tablename__ ="contacts"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    x_link = Column(String)
    linkedin_link = Column(String)
    