from pydantic import BaseModel, EmailStr

class Owner(BaseModel):
   username: str
   email: EmailStr
   password: str
   

class Project(BaseModel):
    title: str
    description: str
    project_link: str
    

class Blog(BaseModel):
    title: str
    content: str
    author: str
    published: int = 0
        
class Contact_Info(BaseModel):
    email: EmailStr
    x_link: str
    linkedin_link : str
        