# FastAPI Boilerplate Project

This is a boilerplate FastAPI project with GitHub OAuth authentication and SQLModel for database management.

## Tech Stack

The tech stack is focussed in simplicity and development speed.

### Backend

- FastAPI: Web framework for building APIs
- SQLModel: ORM for working with SQL databases
- JinjaX: HTML Template engine based on Jinja
- Authlib: Library for OAuth authentication
- Pydantic: Data validation and settings management

### Frontend

- HTMX: Creating SPA like apps in raw HTML
- PicoCSS: Semantic HTML components and modern styling

## Project Structure

```
.
├── app.py            # Main application file
├── auth.py           # Authentication handling
├── config.py         # Configuration settings
├── database.py       # Database connection and operations
├── models.py         # Data models
├── requirements.txt  # Project dependencies
├── static/           # Static files (CSS, JS, etc.)
├── templates/        # JinjaX HTML templates
└── data/             # Database files
    └── data.db       # SQLite database
```

## Configuration

The project uses environment variables for configuration, which are loaded from a `.env` file. Required variables include:

- `APP_URL`: The URL of the application
- `DATABASE_URL`: The database connection URL
- `SESSION_KEY`: Secret key for session management
- `GITHUB_CLIENT_ID`: GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET`: GitHub OAuth client secret

## Running the Application

To run the application, use the following command:

```
python app.py
```

This will start the FastAPI server using Uvicorn, typically on `http://0.0.0.0:8000`.

## Features

- FastAPI for efficient API development
- GitHub OAuth authentication
- SQLModel for database operations
- Jinjax for HTML templating
- Session-based user management
- Basic user dashboard

This boilerplate provides a solid foundation for building web applications with FastAPI, featuring user authentication and database integration.