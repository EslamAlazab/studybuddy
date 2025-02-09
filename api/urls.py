from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomListCreateAPIView.as_view()),
]
