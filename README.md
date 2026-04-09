# KanMind Backend

A RESTful backend for the KanMind project — a Kanban-style task management application. Built with **Django** and **Django REST Framework**.

---

## Tech Stack

| Layer     | Technology                  |
| --------- | --------------------------- |
| Language  | Python 3                    |
| Framework | Django 6.0                  |
| API       | Django REST Framework 3.16  |
| Auth      | Token-based (DRF AuthToken) |
| CORS      | django-cors-headers         |
| Database  | SQLite (default)            |

---

## Project Structure

```
kanmind_backend/
├── core/               # Project settings and root URL config
├── auth_app/           # User registration, login, profiles
├── boards_app/         # Kanban boards management
├── tasks_app/          # Tasks and comments
└── requirements.txt
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd kanmind_backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

---

## Authentication

All endpoints except registration and login require a token in the request header:

```
Authorization: Token <your-token>
```

---

## API Endpoints

### Auth

| Method         | Endpoint                          | Description                          | Auth required |
| -------------- | --------------------------------- | ------------------------------------ | ------------- |
| POST           | `/api/registration/`              | Register a new user                  | No            |
| POST           | `/api/login/`                     | Login and receive auth token         | No            |
| GET            | `/api/email-check/?email=<email>` | Look up a user by email              | Yes           |
| GET            | `/api/auth/profiles/`             | List all user profiles               | Yes           |
| GET/PUT/DELETE | `/api/auth/profiles/<id>/`        | Retrieve, update or delete a profile | Yes           |

#### Registration request body

```json
{
  "email": "user@example.com",
  "password": "secret123",
  "repeated_password": "secret123",
  "fullname": "Jane Doe"
}
```

#### Login request body

```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

#### Login / Registration response

```json
{
  "token": "abc123...",
  "user_id": 1,
  "email": "user@example.com",
  "fullname": "Jane Doe"
}
```

---

### Boards

| Method | Endpoint            | Description                                     |
| ------ | ------------------- | ----------------------------------------------- |
| GET    | `/api/boards/`      | List all boards for the current user            |
| POST   | `/api/boards/`      | Create a new board                              |
| GET    | `/api/boards/<id>/` | Retrieve board details (with members and tasks) |
| PATCH  | `/api/boards/<id>/` | Update board (e.g. add/remove members)          |
| DELETE | `/api/boards/<id>/` | Delete a board (owner only)                     |

---

### Tasks

| Method | Endpoint                                 | Description                                       |
| ------ | ---------------------------------------- | ------------------------------------------------- |
| GET    | `/api/tasks/`                            | List all tasks on accessible boards               |
| POST   | `/api/tasks/`                            | Create a new task                                 |
| GET    | `/api/tasks/<id>/`                       | Retrieve a task                                   |
| PATCH  | `/api/tasks/<id>/`                       | Partially update a task (board cannot be changed) |
| DELETE | `/api/tasks/<id>/`                       | Delete a task (creator or board owner only)       |
| GET    | `/api/tasks/assigned-to-me/`             | List tasks assigned to the current user           |
| GET    | `/api/tasks/reviewing/`                  | List tasks where current user is reviewer         |
| GET    | `/api/tasks/<id>/comments/`              | List all comments on a task                       |
| POST   | `/api/tasks/<id>/comments/`              | Add a comment to a task                           |
| DELETE | `/api/tasks/<id>/comments/<comment_id>/` | Delete a comment (author only)                    |

#### Task fields

| Field         | Type    | Values                                   |
| ------------- | ------- | ---------------------------------------- |
| `status`      | string  | `to-do`, `in-progress`, `review`, `done` |
| `priority`    | string  | `low`, `medium`, `high`, `urgent`        |
| `assignee_id` | integer | User ID                                  |
| `reviewer_id` | integer | User ID                                  |
| `due_date`    | date    | `YYYY-MM-DD`                             |

---

## Permissions Summary

- **Registration & Login** — public
- **All other endpoints** — require a valid auth token
- **Board deletion** — owner only
- **Task deletion** — creator or board owner
- **Comment deletion** — comment author only
- **Board/task access** — restricted to board owners and members
