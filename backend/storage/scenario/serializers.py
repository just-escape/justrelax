from rest_framework.serializers import ModelSerializer

from scenario.models import Scenario, Room, Camera


class ScenarioSerializer(ModelSerializer):
    class Meta:
        model = Scenario
        fields = (
            'id',
            'index',
            'name',
        )


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id',
            'index',
            'scenario',
            'cardinal',
            'channel',
        )


class CameraSerializer(ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            'id',
            'index',
            'room',
            'name',
            'url',
        )
