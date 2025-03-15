# JWT Auth API with Role-Based Access Control (RBAC)

This project is a FastAPI-based backend that uses PostgreSQL and JWT authentication to manage users and projects. It enforces Role-Based Access Control (RBAC) to restrict certain operations to admins only.

---

## Features
- User Registration & Login with hashed passwords (bcrypt)
- JWT-based Authentication
- Role-Based Access Control (RBAC)
  - Admins can create, update, and delete projects
  - Regular users can only read projects
- CRUD Operations for Projects
- PostgreSQL Database with SQLModel ORM

---

## Tech Stack & Dependencies
### Languages & Frameworks:
- Python 3.8+
- FastAPI
- PostgreSQL
- SQLModel (ORM)

### Installed Dependencies:
```sh
fastapi>=0.68.0
sqlmodel>=0.0.4
pydantic>=1.8.2
passlib>=1.7.4
bcrypt>=3.2.0
python-jose>=3.3.0
python-multipart>=0.0.5
psycopg2-binary>=2.9.1
uvicorn>=0.15.0
email-validator>=1.1.3
dotenv
```
Install dependencies using:
```sh
pip install -r requirements.txt
```

---

## Installation & Setup

### 1. Install Python
Ensure Python 3.8+ is installed. Verify using:
```sh
python --version
```

### 2. Clone the Repository
```sh
git clone https://github.com/VishalRayabarapu-01/BackendAssignment.git
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root and add:
```env
DATABASE_URL=postgresql://postgres:password-of-postgres@localhost:5432/jwt_api_db
SECRET_KEY=your-secret-key-here-for-jwt
```

### 4. Initialize the Database
```sh
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

### 5. Start the FastAPI Server
```sh
uvicorn main:app --host 0.0.0.0 --port 8500 --reload
```
---

## API Endpoints

### User Authentication
| Method | Endpoint     | Description |
|--------|------------|-------------|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Authenticate and get JWT token |

### Project Management
| Method  | Endpoint          | Access  | Description |
|---------|-----------------|--------|-------------|
| `GET`   | `/projects`      | All Users  | View all projects |
| `POST`  | `/projects`      | Admin  | Create a new project |
| `PUT`   | `/projects/{id}` | Admin  | Update a project |
| `DELETE`| `/projects/{id}` | Admin  | Delete a project |

---

## Video Demonstration
Watch the setup and usage demo here: https://drive.google.com/file/d/1BG4HpfE6zXMxDdOGjhGhwtaninLm3Q_V/view

---
## Conclusion
This project provides a secure JWT authentication system with RBAC in FastAPI. It's designed for scalability and security while keeping things simple.

