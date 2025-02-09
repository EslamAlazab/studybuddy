from django.contrib.auth import get_user_model
from base.models import Topic, Room, Message


def run():
    User = get_user_model()

    print("Creating default users...")
    user1, created = User.objects.get_or_create(
        email="user1@example.com",
        defaults={"username": "user1", "name": "User One"}
    )
    user2, created = User.objects.get_or_create(
        email="user2@example.com",
        defaults={"username": "user2", "name": "User Two"}
    )

    print("Creating default topics...")
    topic1, created = Topic.objects.get_or_create(name="Django")
    topic2, created = Topic.objects.get_or_create(name="Python")

    print("Creating default rooms...")
    room1, created = Room.objects.get_or_create(
        host=user1,
        topic=topic1,
        name="Django Beginners",
        defaults={"description": "A room for Django beginners!"}
    )
    room2, created = Room.objects.get_or_create(
        host=user2,
        topic=topic2,
        name="Advanced Python",
        defaults={"description": "A room for advanced Python topics!"}
    )

    print("Creating default messages...")
    Message.objects.get_or_create(
        user=user1,
        room=room1,
        defaults={"body": "Hello everyone, welcome to Django learning!"}
    )
    Message.objects.get_or_create(
        user=user2,
        room=room2,
        defaults={"body": "Let's talk about Python optimizations."}
    )

    print("Default data generated successfully!")
