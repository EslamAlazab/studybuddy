# Studybuddy

Studybuddy is an app designed to connect users who share the same academic interests, providing a collaborative environment to study together. Significant focus was placed on query optimization to ensure that each page operates efficiently, maintaining a fixed number of database queries and avoiding N+1 problems.

## Key Features

- **User Registration & Authentication**: Users can sign up, create accounts, and manage their profiles.
- **Room Creation & Joining**: Users can create study rooms for specific subjects or join existing rooms to collaborate with others.
- **Room Comments**: Facilitates discussions through commenting in study rooms, allowing users to engage in focused conversations on topics they are studying together.
- **Pagination**: Allows efficient browsing of Rooms and Topics by breaking down content into pages, improving accessibility and performance.
- **REST API for Study Rooms**: Provides a structured API to interact with study rooms programmatically.

## Tech Stack

- **Django**: A high-level Python web framework for building the app.
- **Django REST Framework (DRF)**: Used for building a RESTful API.\*\*
- **Django ORM**: Utilized for database interactions, with a strong emphasis on optimizing query performance.
- **NGINX**: Acts as a reverse proxy for handling requests efficiently.
- **Gunicorn**: WSGI HTTP server for running the Django application.
- **Docker**: Containerized deployment for easy scalability and management.

## Getting Started

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/yourusername/studybuddy.git
cd studybuddy
```

### 2️⃣ Set Up the Environment

Ensure you have Docker & Docker Compose installed, then run:

```sh
docker-compose up
```

### 3️⃣Create a Superuser

```sh
docker-compose exec django_app python manage.py createsuperuser
```

### 4️⃣ Access the App

Once the services are running, open your browser and go to:

```sh
http://localhost
```
