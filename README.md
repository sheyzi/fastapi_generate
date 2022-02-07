# FastAPI Auth Starter Project

This is a template for FastAPI that comes with authentication preconfigured.

### Technology used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

# Use the template

### Clone the repository

```bash
git clone https://github.com/sheyzi/fastapi_auth.git
```

### Rename the project

```bash
mv fastapi_auth my_new_project
```

### Change project name in core/settings.py

```python
...

class Settings(BaseModel):
    PROJECT_TITLE: str = 'New Project name' # Updated
    PROJECT_VERSION: str = '1.0.0'

...
```

### Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Rename `sample.env` to `.env`

```bash
mv sample.env .env
```

### Get Deta project key

- Open [Deta.sh]('https://www.deta.sh')
- Create an account or login
- In your dashboard click the back arrow beside the deta logo at the top left
- Click on the new project button
- Name your project and select a region
- Copy your project id and project key
- Replace the one in the `.env` file with the one you had just created

### Change secret key

```bash
$ python
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import secrets
>>> secrets.token_hex()
'54e07b3ccd9f38e8601bd01d22537762dcff2c77957b2413ecf97e07e89e815e'
>>>
```

Replace the secret key in the `.env` file with the generated one

### Configure database

Change the postgres sql information with their respective details in the `.env` file

### Migrate the database

```bash
alembic upgrade head
```

### Delete the current git repository

```bash
rm -rf .git
```

### Run the project

```bash
python -m uvicorn main:app --reload
```

### Open api docs

Navigate to [127.0.0.1:8000/docs]('http://127.0.0.1:8000/docs')

### Add field to user model

The template comes without a username field, I will show you how to add that now!

- Edit the `models/users.py` to add the username field

```python
...

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False) # New

...
```

- Reflect db changes on the pydantic schema in the `schemas/users.py`

```python
...

class UserBase(BaseModel):
    email: str
    username: str #New

...
```

- Migrate the database

```bash
$ alembic revision --autogenerate -m "Added username field to users"
$ alembic upgrade head
```

#### Steps to add field to the users db

- Edit the `models/users.py` file
- Reflect changes in `schemas/users.py` file
- Migrate database

### How to use the authentication

- Import the `get_active_users` dependency from the `core/dependency.py`

```python
from core.dependency import get_active_user
```

- Import the `Depends` function from `fastapi`

```python
from fastapi import Depends
```

- Import the `UserOut` class from the `schemas/users.py`

```python
from schemas.users import UserOut
```

- Add the dependency to the route function

```python
...

@auth_router.post("/some-route/")
def register_user(current_user: UserOut = Depends(get_active_user)):

...
```

### How to create custom auth permissions

In this section we will create a permission for only admins

In `core/dependency.py` add

```python
...

def get_admin_user(current_user: UserOut = Depends(get_active_user)):
    if not current_user.is_admin:
        raise HTTPException("Not an admin user!")
    return current_user

...
```
