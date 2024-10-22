# FastAPI Docker PostgreSQL JWT Authentication

A simple project setup using **FastAPI**, **Docker**, and **PostgreSQL** with **JWT** authentication. This project demonstrates how to create a basic FastAPI application with a PostgreSQL database, containerized using Docker, and secured with JSON Web Tokens (JWT) for authentication.

## 🚀 Features

- **FastAPI**: High-performance web framework for building APIs.
- **Docker**: Containerized environment for easy deployment.
- **PostgreSQL**: Reliable and robust relational database system.
- **JWT Authentication**: Secure API access with JSON Web Tokens.


## 🛠 Technologies Used
- **FastAPI**: For building the backend API.
- **PostgreSQL**: For database management.
- **Docker**: For creating reproducible environments.
- **JWT**: For authentication and authorization.

## 🚀 Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Clone the Repository

```
git clone https://github.com/YsrajSingh/fastapi-docker-postgres-jwt-auth.git
cd fastapi-docker-postgres-jwt-auth
```

### Build and Run the Project
Build the Docker containers and start the application:

```
docker-compose up --build
```

This will start:

- FastAPI app on ```http://localhost:8000```
- pgAdmin for managing PostgreSQL on ```http://localhost:5050```


### Accessing the Application
- **FastAPI Documentation**: ```http://localhost:8000/docs```
- **pgAdmin**: Login with the credentials specified in the ```.env``` file (```admin@example.com``` / ```admin_password```).

### JWT Authentication
To authenticate and get a token:

1. Send a **POST** request to ```/token``` with your username and password.
1. Use the obtained JWT token for accessing protected routes.

    Example request to get JWT token:

    ```
    curl -X 'POST' \
    'http://localhost:8000/token' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=testuser&password=testpassword'
    ```


**Example API Usage**
- **GET /users**: Get list of users (requires JWT token).
- **POST /users**: Create a new user (requires JWT token).

## 🧑‍💻 Development

If you want to make changes or contribute, you can use the following steps to set up the development environment.

1. **Install dependencies**:
    - You can install FastAPI and other dependencies inside the Docker container by using:
        ```
        docker exec -it fastapi-app pip install -r requirements.txt
        ```
1. **Run migrations** (for PostgreSQL):
Run the following command to apply database migrations:

    ```
    docker exec -it fastapi-app python3 manage.py migrate
    ```



## 🔧 Configuration

The environment variables are managed in the ```.env``` file:

```
POSTGRES_DB=defaultdb
POSTGRES_USER=root
POSTGRES_PASSWORD=root123
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin_password
PGADMIN_DEFAULT_PORT=5432

SECRET_KEY=<your_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=525960
```



