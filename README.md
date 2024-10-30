# Studybuddy

Studybuddy is an app designed to connect users who share the same academic interests, providing a collaborative environment to study together. Significant focus was placed on query optimization to ensure that each page operates efficiently, maintaining a fixed number of database queries and avoiding N+1 problems.

## Key Features

- User Registration: Users can sign up, create accounts, and manage their profiles.
- Room Creation & Joining: Users can create study rooms for specific subjects or join existing rooms to collaborate with others.
- Room Comments: Facilitates discussions through commenting in study rooms, allowing users to engage in focused conversations on topics they are studying together.
- Pagination: Allows efficient browsing of Rooms and Topics by breaking down content into pages, improving accessibility and performance.

## Tools & Technologies

- Django: A high-level Python web framework for building the app.
- Django ORM: Utilized for database interactions, with a strong emphasis on optimizing query performance.
