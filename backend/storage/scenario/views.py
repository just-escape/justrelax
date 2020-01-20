from rest_framework.viewsets import ModelViewSet

from scenario.models import Scenario, Room, Camera
from scenario.serializers import ScenarioSerializer, RoomSerializer
from scenario.serializers import CameraSerializer


class ScenarioView(ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    ordering_fields = ('index',)
    ordering = ('index',)


class RoomView(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ('scenario',)
    ordering_fields = ('index',)
    ordering = ('index',)


class CameraView(ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    filterset_fields = ('room',)
    ordering_fields = ('index',)
    ordering = ('index',)
