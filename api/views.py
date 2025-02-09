from rest_framework import generics
from api.serializers import RoomListSerializer, RoomCreateSerializer
from base.models import Room
from rest_framework.response import Response


class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.select_related('host', 'topic').only(
        'id', 'name', 'joined_count', 'created',
        'host__id', 'host__username', 'host__avatar',
        'topic__name'
    )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoomCreateSerializer
        return RoomListSerializer

    # def get(self, request):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = {
    #         "count": queryset.count(),  # Count of rooms
    #         "rooms": serializer.data,   # Serialized room data
    #     }
    #     return Response(data)


class RoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.prefetch_related(
        'participants').select_related('host', 'topic')
