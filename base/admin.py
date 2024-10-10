from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import User, Topic, Room, Message


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profiles'


# class Custom(UserAdmin):
#     inlines = (ProfileInline,)


# admin.site.unregister(User)
# admin.site.register(User, Custom)

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
