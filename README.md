# Beds2Bytes Backend Service

Backend service for the *Beds2Bytes* virtual care web application. 

## Overview

This service provides the core backend functionality for the application, including:

- REST API (CRUD Operations)
- Websocket Server
- Authentication
- Image/File handler

## Architecture

The backend consists of:

- REST API for handling client requests and database operations
- WebSocket server for real-time communication
- Authentication layer using JWT for secure access
- Database layer for persistent storage

## Tech Stack

- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy

## Requirements

See `requirements.txt` for the full list of dependencies.

### Key Packages

- fastapi
- fastapi-cors
- pydantic
- uvicorn
- sqlalchemy
- psycopg2-binary
- python-dotenv
- requests
- python-jose
- passlib[argon2]

### Other Software

Docker (Optional)

The docker compose file maps the 8080 port for usage, but you don't have to do anything else for now. 

## Getting Started

### Prerequisites

- Python 3.11
- PostgreSQL instance (local or remote)
- (Optional) Docker
 
1. Clone the repository

```bash
git clone [gitlink]
cd backend
```

2. Create a virtual environment

```bash
python -m venv 'your_venv_name'
```

And activate the environment

Linux/macOS
```bash
source venv/bin/activate
```
Windows
```bash
venv\Scripts\activate
```

3. Install the Dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Environment Variables

Create a .env file in the root directory (recommended to just copy the .env_example file and rename it .env).

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

The API will be available at:

http://localhost:8000 

6. Run with Docker (Optional)

The repository includes all the relevant docker files to work with docker. Just run:

```bash
docker compose up
```
The API will be available at:

http://localhost:8080 

(The ports can be configured to your prefered port)

## API Documentation 

Once the service is running, interactive API docs are available at:

Swagger UI: `http://localhost:8080/docs`

## Project Structure

```
backend/
├── requirements.txt         # Dependencies
├── Dockerfile               # Docker container setup
├── docker-compose.yml       # Docker configuration
├── .env                     # Environment variables (not committed)
└── app/
    ├── main.py              # Entry point of the application
    ├── config.py            # Configurations
    ├── constants.py         # Global constants
    ├── routers/             # API route definitions
    ├── security/            # JWT Authentication
    ├── database/            # Database setup and connection and models/schemas
    └── websocket/           # Websocket server configuration/endpoint
```
