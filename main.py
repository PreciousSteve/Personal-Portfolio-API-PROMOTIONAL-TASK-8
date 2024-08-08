# Personal Portfolio API:

# Develop a fully functional API for a personal portfolio website, including endpoints for projects (add, edit, delete,all project, single project),
# blog posts (add, edit, delete,all blog posts, single blog post), and contact information (add, edit, delete). 
# Use SQLite as a database. 
# Document the API endpoints and push your codes to your github repository. 

# SUBMISSION CRITERIA:
# Submit your github repository link 

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import models, schemas
from app import crud
from app.db import engine, db_session

app = FastAPI()

security_detail = OAuth2PasswordBearer(tokenUrl="login")

models.Base.metadata.create_all(bind=engine)

def get_session():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
        
        

@app.post("/signup")
def create_owner(owner:schemas.Owner, session=Depends(get_session)):
    existing_owner = crud.check_email(session, owner.email)
    if existing_owner:
        raise HTTPException(status_code=409,
                            detail="Owner already exists")
    else:
        new_owner = crud.create_owner(session, owner)
    return new_owner

"""
    This endpoint creates a new owner by checking if the owner already exists based on the email
    provided.
    
    :param owner: The `owner` parameter in the `create_owner` function is of type `schemas.Owner`, which
    is a Pydantic model representing the data structure of an owner. It contains information such
    as the owner's email, username, password. This parameter is used to create a new owner
    :type owner: schemas.Owner
    :param session: The `session` parameter in the `create_owner` function is used to manage the
    database session. It is a dependency that is injected into the function using
    `Depends(get_session)`. This allows the function to interact with the database by executing queries
    and transactions within the provided session context. 
    :return: the newly created owner if the owner does not already exist in the database. If the owner
    already exists, it will raise an HTTPException with a status code of 409 and a detail message
    indicating that the owner already exists.
"""
        
        
@app.post("/login")
def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(), session = Depends(get_session)):
    owner = crud.authenticate_owner(session, form_data.username, form_data.password)
    if not owner:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = form_data.username
    return {"access_token": access_token, "token_type": "bearer"}

"""
    This endpoint handles user authentication for generating access tokens.
    
    :param form_data: The `form_data` parameter in is type `OAuth2PasswordRequestForm`. It is used to extract the username and password from the request body
    when a user tries to log in. The `form_data` object will contain the username and password provided
    by
    :type form_data: OAuth2PasswordRequestForm
    :param session: The `session` parameter in the `login_for_access_token` function is used to manage
    the database session. It is obtained using the `Depends` function with the `get_session` dependency,
    which likely provides a database session for interacting with the database within the function. 
    :return: The code is returning a dictionary containing the access token and token type. The access
    token is set to the username provided in the form data, and the token type is set to "bearer".
"""


@app.get("/owner/me")
def owners_me(token = Depends(security_detail), session = Depends(get_session)):
    owner = crud.get_owner_by_username(session, token)
    if not owner:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message":f'Hello, {owner.username}'}

"""
    The endpoint here retrieves the owner information based on the provided token and session,
    returning an HTTP 401 error if the owner is not found.
    
    :param token: The `token` parameter in the `owners_me` function is obtained using the `Depends`
    function with the `security_detail` dependency. This means that the `security_detail`
    dependency is responsible for extracting and validating the token from the request. The token is
    used to identify the user
    :param session: The `session` parameter in the `owners_me` function is likely used to interact with
    the database session. It is obtained by calling the `get_session` dependency, which probably sets up
    and provides a database session for the function to use when querying the database.
    :return: The function `owners_me` is returning the owner object retrieved from the database based on
    the username provided in the token. If the owner is not found, it raises an HTTPException with a
    status code of 401 and the detail "Invalid credentials".
"""
        

# For projects
@app.post("/projects/")
def create_project(project: schemas.Project, session = Depends(get_session)):
    return crud.create_project(session=session, project=project)

"""
    This endpoint creates a new project using the provided project data in the database.
    
    :param project: The `project` parameter in the `create_project` function is of type
    `schemas.Project`, which represents the data structure or schema expected for a project. It
    is being passed as part of the request body when creating a new project
    :type project: schemas.Project
    :param session: The `session` parameter in the `create_project` function is used to manage the
    database session. It is typically passed as a dependency using `Depends(get_session)`, where
    `get_session` is a function that provides a database session for the request.
    :return: The code is returning the result of creating a new project using the `create_project`
    function from the `crud` module. The `create_project` function takes the database session and the
    project data as input parameters and is responsible for adding the new project to the database. The
    result returned by this function could be the newly created project object or an indication of the
    success/failure of the creation process.
    """

@app.get("/projects/")
def read_projects(session = Depends(get_session)):
    return crud.get_all_projects(session=session)

"""
    This endpoint that retrieves all projects from a database using a session dependency.
    
    :param session: The `session` parameter in the `read_projects` function is a dependency that is
    injected using `Depends(get_session)`. This dependency is used to obtain a database session that
    allows the function to interact with the database when retrieving all projects
    :return: The code is returning all projects from the database by calling the `get_all_projects`
    function from the `crud` module.
"""


@app.get("/projects/{project_id}")
def read_project(project_id: int, session = Depends(get_session)):
    project = crud.get_single_project(session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

"""
    This endpoint reads a project with a specific ID from a database.
    
    :param project_id: The `project_id` parameter in the `read_project` function is used to specify the
    unique identifier of the project that the user wants to retrieve information about. This parameter
    is part of the URL path and is expected to be an integer value. 
    :type project_id: int
    :param session: The `session` parameter in the `read_project` function is a dependency that is
    obtained using the `Depends` function from FastAPI. It is used to get a database session object that
    allows the function to interact with the database. 
    :return: The code is returning the project details for the project with the specified `project_id`.
    If the project is not found in the database, it raises an HTTP 404 error with the message "Project
    not found".
"""


@app.put("/projects/{project_id}")
def update_project(project_id: int, project: schemas.Project, session = Depends(get_session)):
    updated_project = crud.edit_project(session=session, project_id=project_id, project=project)
    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

"""
    This endpoint updates a project with the specified project ID using the provided project
    data.
    
    :param project_id: The `project_id` parameter in the `update_project` function represents the unique
    identifier of the project that you want to update. It is specified in the URL path of the PUT
    request ("/projects/{project_id}"). This parameter is of type integer (`int`) as indicated by the
    type hint in
    :type project_id: int
    :param project: The `project` parameter in the `update_project` function is of type
    `schemas.Project`, which likely represents the data structure or schema for a project in your
    application.
    :type project: schemas.Project
    :param session: The `session` parameter in the `update_project` function is used to pass the
    database session to the function. This allows the function to interact with the database to update
    the project information. The `get_session` function is a dependency that provides the
    database session to the route function
    :return: The function `update_project` is returning the updated project after editing it in the
    database. If the project is not found, it will raise an HTTPException with a status code of 404 and
    the detail message "Project not found".
"""


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, session = Depends(get_session)):
    deleted_project = crud.delete_project(session=session, project_id=project_id)
    if deleted_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return deleted_project

"""
    This endpoint deletes a project with a specified project ID and returns the deleted project if
    found.
    
    :param project_id: The `project_id` parameter in the `delete_project` function is the unique
    identifier of the project that you want to delete. This parameter is passed in the URL path as part
    of the route definition `/projects/{project_id}` and is expected to be an integer value
    :type project_id: int
    :param session: The `session` parameter in the `delete_project` function is a dependency that is
    obtained using the `Depends` function from FastAPI. It is used to interact with the database session
    to perform operations like deleting a project with the specified `project_id`. 
    :return: The `delete_project` function is returning the deleted project. If the project with the
    specified `project_id` is not found, it raises an HTTPException with a status code of 404 and the
    detail message "Project not found".
"""


@app.delete("/projects/")
def delete_all_projects(session = Depends(get_session)):
    crud.delete_all_projects(session=session)
    return {"detail": "All projects deleted"}

"""
    This endpoint deletes all projects from the database and returns a message confirming the deletion.
    
    :param session: The `session` parameter in the `delete_all_projects` function is a dependency that
    is injected using `Depends(get_session)`. This dependency is used to obtain a database session that
    allows the function to interact with the database to delete all projects. The `get_session` function
    likely provides a database
    :return: The function `delete_all_projects` is returning a dictionary with the key "detail" and the
    value "All projects deleted".
"""

# Blog
@app.post("/blogs/")
def create_blog(blog: schemas.Blog, session = Depends(get_session)):
    return crud.create_blog(session=session, blog=blog)
"""
    This endpoint creates a new blog by calling the `create_blog` function from the `crud` module
    with the provided blog data and session.
    
    :param blog: The `blog` parameter in the `create_blog` function is of type `schemas.Blog`, which is a Pydantic model representing the structure of a blog. When a POST request is made to the
    `/blogs/` endpoint with a JSON payload representing a blog, this function will be
    :type blog: schemas.Blog
    :param session: The `session` parameter in the `create_blog` function is used to manage the database
    session. It is typically a database session object that allows the function to interact with the
    database to create a new blog entry. 
    :return: The code is returning the result of creating a blog using the `create_blog` function from
    the `crud` module. The `create_blog` function takes the `session` and `blog` as parameters and is
    responsible for creating a new blog entry in the database.
"""



@app.get("/blogs/")
def read_blogs(session = Depends(get_session)):
    return crud.get_all_blogs(session=session)
"""
    This endpoint retrieves all blogs from a database
    using a session dependency.
    
    :param session: The `session` parameter in the `read_blogs` function is a dependency that is
    injected using `Depends(get_session)`. This dependency is used to obtain a database session that
    allows the function to interact with the database to retrieve all blogs using the
    `crud.get_all_blogs` function
    :return: The code is returning all the blogs by calling the `get_all_blogs` function from the `crud`
    module using the session provided as a dependency.
"""


@app.get("/blogs/{blog_id}")
def read_project(blog_id: int, session = Depends(get_session)):
    blog = crud.get_single_blog(session=session, blog_id=blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
"""
    This endpoint reads a single blog post based on the provided blog ID.
    
    :param blog_id: The `blog_id` parameter in the code snippet represents the unique identifier of a
    blog. It is used to retrieve a specific blog from the database by its ID
    :type blog_id: int
    :param session: The `session` parameter in the `read_project` function is a dependency that is
    obtained using the `Depends` function from. It is used to get a database session object that
    allows the function to interact with the database.
    :return: The code is returning a single blog post with the specified `blog_id`. If the blog post is
    not found, a 404 HTTP error with the message "Blog not found" will be raised.
"""


@app.put("/blogs/{blog_id}")
def update_blog(blog_id: int, blog: schemas.Blog, session = Depends(get_session)):
    updated_blog = crud.edit_blog(session=session, blog_id=blog_id, blog=blog)
    if updated_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog

"""
    This endpoint updates a blog with the specified ID.
    
    :param blog_id: The `blog_id` parameter in the `update_blog` function represents the unique
    identifier of the blog that needs to be updated. It is passed as a path parameter in the URL of the
    PUT request to specify which blog is being updated
    :type blog_id: int
    :param blog: The `blog` parameter in the `update_blog` function represents the data of the blog that
    is being updated. It is of type `schemas.Blog`, which corresponds to a Pydantic model defined
    in the `schemas` module. When this function is called, the `blog` data
    :type blog: schemas.Blog
    :param session: The `session` parameter in the `update_blog` function is used to pass the database
    session to the function. This allows the function to interact with the database to update the blog
    information. The `session` parameter is obtained using the `get_session` dependency.
    :return: The function `update_blog` is returning the updated blog after editing it in the database.
    If the blog is not found, it will raise an HTTPException with a status code of 404 and the detail
    message "Blog not found".
"""

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, session = Depends(get_session)):
    deleted_blog = crud.delete_blog(session=session, blog_id=blog_id)
    if deleted_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return deleted_blog
"""
    This endpoint deletes a blog with a specified ID and returns the deleted blog if found, otherwise
    raises a 404 error.
    
    :param blog_id: The `blog_id` parameter in the `delete_blog` function represents the unique
    identifier of the blog that is to be deleted. This parameter is passed in the URL path as part of
    the route definition `/blogs/{blog_id}` and is expected to be an integer value
    :type blog_id: int
    :param session: The `session` parameter in the `delete_blog` function is a dependency that is
    obtained using the `Depends` function. It is used to interact with the database session to perform
    operations like deleting a blog entry.
    :return: the deleted blog. If the blog with the specified `blog_id` is not found, it raises an
    HTTPException with a status code of 404 and the detail "Blog not found".
"""


@app.delete("/blogs/")
def delete_all_blogs(session = Depends(get_session)):
    crud.delete_all_blogs(session=session)
    return {"detail": "All blogs deleted"}
"""
    This function deletes all blogs from the database.
    
    :param session: The `session` parameter in the `delete_all_blogs` function is a dependency that is
    injected using `Depends(get_session)`. This dependency is used to obtain a database session for
    interacting with the database.
    :return: a dictionary with a key "detail" and a value "All blogs deleted".
"""

#contact information

@app.post("/contacts/")
def create_contact(contact: schemas.Contact_Info, session = Depends(get_session)):
    return crud.create_contact(session=session, contact=contact)
"""
    This endpoint creates a new contact using the provided contact information in the database.
    
    :param contact: The `contact` parameter in the `create_contact` function is of type
    `schemas.Contact_Info`. This means that the function expects to receive a data structure that
    conforms to the schema defined in the `schemas.py` file for the `Contact_Info` class.
    :type contact: schemas.Contact_Info
    :param session: The `session` parameter in the `create_contact` function is used to pass the
    database session to the function. This allows the function to interact with the database, such as
    creating a new contact record using the provided contact information. The `session` parameter is
    obtained using the `get_session` dependency.
    :return: The function `create_contact` is returning the result of calling the `create_contact`
    function from the `crud` module with the provided `session` and `contact` parameters.
"""


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: schemas.Contact_Info, session = Depends(get_session)):
    updated_contact = crud.edit_contact(session=session, contact_id=contact_id, contact=contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact Info not found")
    return updated_contact
"""
    This endpoint updates a contact's information in a database using the provided contact ID and
    contact information.
    
    :param contact_id: The `contact_id` parameter in the function `update_contact` is of type integer
    and represents the unique identifier of the contact that needs to be updated. 
    :type contact_id: int
    :param contact: The `contact` parameter in the `update_contact` function is of type
    `schemas.Contact_Info`. This parameter likely represents the updated contact information that will
    be used to update the contact with the specified `contact_id`. The `schemas.Contact_Info` is
    expected to contain the necessary fields and data to update
    :type contact: schemas.Contact_Info
    :param session: The `session` parameter in the function `update_contact` is used to pass the
    database session to the function. This allows the function to interact with the database to update
    the contact information specified by the `contact_id`.
    :return: the updated contact information after editing it in the database. If the contact
    information is not found, it will raise an HTTPException with a status code of 404 and the detail
    message "Contact Info not found".
"""




@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, session = Depends(get_session)):
    deleted_contact = crud.delete_contact(session=session, contact_id=contact_id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact info not found")
    return deleted_contact
"""
    This endpoint deletes a contact with a specified ID and returns the deleted contact information,
    raising a 404 error if the contact is not found.
    
    :param contact_id: The `contact_id` parameter represents the unique identifier
    of the contact that you want to delete. This identifier is used to locate and delete the specific
    contact from the database
    :type contact_id: int
    :param session: The `session` parameter is used to represent the database session that is being
    passed to the `delete_contact` function. It is typically used to interact with the database and
    perform operations such as deleting a contact with the specified `contact_id`.
    :return: the deleted contact information. If the contact with the specified contact_id is not found
    in the database, it will raise an HTTPException with a status code of 404 and the detail message
    "Contact info not found".
"""