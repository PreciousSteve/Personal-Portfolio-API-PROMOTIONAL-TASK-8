from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_owner(session, owner):
    hashed_password = get_password_hash(owner.password)
    new_owner = models.Owner(username=owner.username,
                             email=owner.email,
                             hashed_password = hashed_password)
    session.add(new_owner)
    session.commit()
    session.refresh(new_owner)
    
    return new_owner


def check_email(session, email):
    owner = session.query(models.Owner).filter(models.Owner.email == email).first()
    return owner


def authenticate_owner(session, username, password):
    owner = session.query(models.Owner).filter(models.Owner.username == username).first()
    if owner and verify_password(password, owner.hashed_password):
        return owner
   

def get_owner_by_username(session, username):
    return session.query(models.Owner).filter(models.Owner.username == username).first()

# for project
def create_project(session, project):
    new_project = models.Project(title=project.title, description=project.description, project_link=project.project_link)
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project


def get_all_projects(session):
    return session.query(models.Project).all()


def get_single_project(session, project_id):
    return session.query(models.Project).filter(models.Project.id == project_id).first()


def edit_project(session, project_id, project):
    add_project = session.query(models.Project).filter(models.Project.id == project_id).first()
    if not add_project:
        return None
    for key, value in project.dict().items():
        setattr(add_project, key, value)
    session.commit()
    session.refresh(add_project)
    return add_project


def delete_project(session, project_id):
    project = session.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return None
    session.delete(project)
    session.commit()
    return project


def delete_all_projects(session):
    session.query(models.Project).delete()
    session.commit()
    
    
# for blog
def create_blog(session, blog):
    new_blog = models.Blog(title=blog.title, content=blog.content, author=blog.author, published=blog.published)
    session.add(new_blog)
    session.commit()
    session.refresh(new_blog)
    
    return new_blog


def get_all_blogs(session):
    return session.query(models.Blog).all()

def get_single_blog(session, blog_id):
    return session.query(models.Blog).filter(models.Blog.id == blog_id).first()


def edit_blog(session, blog_id, blog):
    edit_blog = session.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not edit_blog:
        return None
    for key, value in blog.dict().items():
        setattr(edit_blog, key, value)
    session.commit()
    session.refresh(edit_blog)
    return edit_blog


def delete_blog(session, blog_id):
    blog = session.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        return None
    session.delete(blog)
    session.commit()
    return blog


def delete_all_blogs(session):
    session.query(models.Blog).delete()
    session.commit()
    
    
#contact
def create_contact(session, contact):
    new_contact = models.Contact_Info(email=contact.email, x_link=contact.x_link, linkedin_link=contact.linkedin_link)
    session.add(new_contact)
    session.commit()
    session.refresh(new_contact)
    
    return new_contact


def edit_contact(session, contact_id: int, contact):
    edited_contact = session.query(models.Contact_Info).filter(models.Contact_Info.id == contact_id).first()
    if not edited_contact:
        return None
    for key, value in contact.dict().items():
        setattr(edited_contact, key, value)
    session.commit()
    session.refresh(edited_contact)
    return edited_contact

def delete_contact(session, contact_id: int):
    contact = session.query(models.Contact_Info).filter(models.Contact_Info.id == contact_id).first()
    if not contact:
        return None
    session.delete(contact)
    session.commit()
    return contact
