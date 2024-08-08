# Personal Portfolio API

## Overview

The **Personal Portfolio API** is a FastAPI-based backend service designed to manage and showcase a personal portfolio website. It provides endpoints for handling projects, blog posts, and contact information, using SQLite as the database. This API allows for CRUD (Create, Read, Update, Delete) operations, making it a comprehensive solution for portfolio management.

## Features

- **Projects**: Add, edit, delete, and view all or single projects.
- **Blog Posts**: Add, edit, delete, and view all or single blog posts.
- **Contact Information**: Add, edit, and delete contact information.
- **Authentication**: Secure endpoints with basic authentication.

## Getting Started

### Prerequisites

- Python 3.7 or later
- pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/personal-portfolio-api.git
   cd personal-portfolio-api
2. **Create and activate a virtual environment:**
   
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. **Install dependencies:**

pip install -r requirements.txt

### Running the API
**Start the application:**

uvicorn app.main:app --reload

The application will be available at http://127.0.0.1:8000.

**Access the API documentation:**

OpenAPI docs: http://127.0.0.1:8000/docs
Alternative Swagger UI: http://127.0.0.1:8000/redoc


