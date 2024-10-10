from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<int:pk>', views.user_profile, name='user-profile'),
    path('edit-user', views.edit_user, name='edit-user'),
    path('login', views.user_login, name='login'),
    path('register', views.user_register, name='register'),
    path('logout', views.logout, name='logout'),
    path('create-room', views.create_room, name='create-room'),
    path('update-room/<int:pk>', views.update_room, name='update-room'),
    path('delete-room/<int:pk>', views.delete_room, name='delete-room'),
    path('room/<int:pk>', views.get_room, name='get-room'),
    path('delete-message/<int:pk>', views.delete_message, name='delete-message'),
    path('activity', views.activity_page, name='activity'),
    path('topics', views.topics_page, name='topics'),
]
