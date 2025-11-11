# backend

Running with FastApi for the REST API

POSTGRESQL as Database

Hosted on CSC!

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

The docker files are meaningless for local development so they can be deleted if one wishes to or used with a dockerized development environment.
