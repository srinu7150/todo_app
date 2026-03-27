# Todo Application

A full-featured Todo Web Application built with **Flask** and **PostgreSQL**, featuring a modern web interface, user authentication, and complete CRUD operations.

## Features

- ✅ **User Authentication** - Register, login/logout with session-based authentication
- ✅ **Todo CRUD Operations** - Create, Read, Update, Delete todos via web interface
- ✅ **Authorization** - Each user can only access their own todos
- ✅ **Web Interface** - Beautiful responsive UI with HTML templates
- ✅ **Database Persistence** - PostgreSQL with SQLAlchemy ORM
- ✅ **Input Validation** - Form validation and error handling
- ✅ **Production Ready** - Connection pooling, error handling, CORS support

## Project Structure

```
todo_app/
├── app/
│   ├── __init__.py
│   ├── auth.py          # Authentication functions
│   ├── flask_app.py     # Flask application with routes and models
│   └── main.py          # Application entry point
├── database/
│   ├── config.py        # Database connection setup
│   └── models.py        # SQLAlchemy models (User, Todo)
├── migrations/
│   └── 001_initial_schema.sql  # Initial SQL migration
├── static/
│   ├── css/
│   │   └── style.css    # Application styles
│   └── js/
│       └── app.js       # Client-side JavaScript
├── templates/           # HTML templates for web pages
│   ├── base.html        # Base template with layout
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # Dashboard showing todos
│   ├── add_todo.html    # Add new todo form
│   ├── edit_todo.html   # Edit todo form
│   ├── stats.html       # Statistics page
│   ├── 404.html         # 404 error page
│   └── 500.html         # 500 error page
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
└── pg_db.yaml          # Docker Compose database configuration
```

## Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose** (for PostgreSQL)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL Database

```bash
docker compose up -d
```

This will start:
- PostgreSQL on port `5432`
- PGAdmin on port `5050` (http://localhost:5050)

### 3. Initialize Database

The database tables are automatically created when the app starts. For manual initialization:

```bash
python app/flask_app.py
```

Or run the SQL migration directly:

```bash
psql -h localhost -U admin -d todo_db -f migrations/001_initial_schema.sql
```

### 4. Run the Application

```bash
source .venv/bin/activate && python app/flask_app.py
```

The web application will be available at `http://localhost:5000` (default Flask port)

## Web Pages

- **Home**: Redirects to dashboard if logged in, login page otherwise
- **Login**: `/login` - User login page
- **Register**: `/register` - New user registration
- **Dashboard**: `/dashboard` - View all your todos
- **Add Todo**: `/todo/add` - Create a new todo item
- **Stats**: `/stats` - View statistics about your todos

## Web Features

### Authentication Flow

1. Register a new account at `/register`
2. Login with credentials at `/login`
3. Access protected routes (dashboard, add todo, etc.)
4. Logout from any page using the logout button

### Todo Management

- Create new todos with title and description
- Mark todos as completed/incomplete
- Edit existing todos
- Delete todos
- View statistics (total, completed, pending)

## Configuration

Environment variables (optional):

```bash
export SECRET_KEY="your-secret-key-change-in-production"
export DEBUG="true"
```

## Database Connection

The application connects to PostgreSQL using the connection string in `app/flask_app.py`:

```
postgresql://admin:admin123@localhost:5432/todo_db
```

## Security Notes

- Change the default `SECRET_KEY` in production
- Use strong passwords (minimum 8 characters)
- Configure CORS appropriately for production
- Enable DEBUG=False in production

## License

MIT License
