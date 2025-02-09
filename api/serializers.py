from rest_framework import serializers
from base.models import Room, User


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'description', 'host', 'topic']


class RoomHostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.ImageField()


class RoomListSerializer(serializers.ModelSerializer):
    host = RoomHostSerializer()
    topic = serializers.CharField(source='topic.name')

    class Meta:
        model = Room
        fields = ['name', 'host', 'topic', 'joined_count', 'created']


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email',
                  'bio', 'is_active', 'avatar', 'date_joined']
