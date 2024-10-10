from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Topic, Room, Message


class MyUserCreationForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
