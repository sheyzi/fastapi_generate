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
