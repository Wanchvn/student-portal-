# Student Portal Application

A full-stack Student Portal web application built with Python Flask, SQLAlchemy, Bootstrap 5, and JavaScript (ES6).

## Features

- Student registration with personal and academic information
- Profile/passport image upload (JPG, JPEG, PNG)
- View all registered students in a responsive table
- View individual student details
- Update admission status asynchronously via AJAX (Fetch API)
- Dynamic department and programme select boxes loaded from REST API

## Tech Stack

| Layer    | Technology                          |
| -------- | ----------------------------------- |
| Backend  | Python 3.x, Flask, Flask-SQLAlchemy |
| Database | SQLite                              |
| Frontend | HTML5, CSS3, JavaScript (ES6), Bootstrap 5 |

## Project Structure

```
student_portal/
├── app.py                 # Application entry point
├── models.py              # SQLAlchemy Student model
├── config.py              # Configuration settings
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── routes/
│   ├── web.py             # Web page routes (Blueprint)
│   └── api.py             # REST API routes (Blueprint)
├── static/
│   ├── css/style.css
│   ├── js/main.js, register.js, details.js
│   ├── images/
│   └── uploads/           # Uploaded student photos
├── templates/             # Jinja2 HTML templates
└── database/              # SQLite database file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python init_db.py
```

This creates the SQLite database at `database/student_portal.db` with the `students` table.

> **Note:** The database is also auto-created when you run `app.py` for the first time.

### 5. Run the Application

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

## Routes

| Method | Route                        | Description                    |
| ------ | ---------------------------- | ------------------------------ |
| GET    | `/`                          | Landing page                   |
| GET    | `/register`                  | Registration form              |
| POST   | `/register`                  | Submit registration            |
| GET    | `/students`                  | Students index table           |
| GET    | `/student/<id>`              | Student details page           |
| GET    | `/api/departments`           | JSON list of departments       |
| GET    | `/api/programmes`            | JSON list of programmes        |
| POST   | `/api/update-status/<id>`    | Update admission status (AJAX) |

## API Examples

### Get Departments

```
GET /api/departments
```

Response:

```json
[
  {"id": 1, "name": "Computer Science"},
  {"id": 2, "name": "Information Technology"},
  {"id": 3, "name": "Cyber Security"},
  {"id": 4, "name": "Networking"}
]
```

### Update Admission Status

```
POST /api/update-status/1
Content-Type: application/json

{"status": "Admitted"}
```

Response:

```json
{"success": true}
```

## Security

- Uploaded file types validated (JPG, JPEG, PNG only)
- `secure_filename()` used for all uploads
- SQLAlchemy ORM prevents SQL injection
- Server-side and client-side form validation
- Maximum upload size: 5 MB

## License

© 2026 Student Portal Application. All Rights Reserved.
