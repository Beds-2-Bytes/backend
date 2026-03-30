# backend

Running with FastApi for the REST API

## Requirements

### Language

Python 3.11

### Packages

FastAPI

FastAPI-cors

pydantic

uvicorn

SQLAlchemy

psycopg2-binary

python-dotenv

requests

python-jose

passlib[argon2]

### Database

PostgreSQL

### Other Software

Docker

The docker compose file maps the 8080 port for usage, but you don't have to do anything else for now. 

## Use locally

Python 3.11 used in this project.

You need to have a postgresql server instance in use, for development a local docker instance och pgsql was used.

1. Clone repository

```Python
git clone [gitlink]
cd backend
```

2. Create python virtual environment

```Python
python -m venv 'your_venv_name'
```

And activate the environment

3. Install the dependencies:

```Python
pip install -r requirements.txt
```

4. Configure .env file

```bash
MODE=development

DBNAME='db_name'

DBPW='db_password'

DBUSER='db_user'

DBURL='your_db_url, if local then localhost:5432'

SECRETKEY='your_jwt_secret'
```

5. Run the application!

```Python
fastapi dev main.py
```
