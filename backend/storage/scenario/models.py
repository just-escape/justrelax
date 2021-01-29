from django.db import models
from django import forms


class Scenario(models.Model):
    name = models.CharField(max_length=64)
    index = models.IntegerField(unique=True)


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ('name', 'index',)


class Room(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    cardinal = models.CharField(max_length=16, null=True, blank=True)
    channel = models.CharField(max_length=64)
    index = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['scenario', 'index'],
                name='scenario_index',
            ),
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('scenario', 'cardinal', 'channel', 'index',)


CAMERA_TYPES = (
    ('mjpeg', 'MJPEG'),
    ('webrtc_janus', 'WebRTC (Janus)'),
)


class Camera(models.Model):
    name = models.CharField(max_length=64)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    index = models.IntegerField()
    type = models.CharField(max_length=64, choices=CAMERA_TYPES, default=CAMERA_TYPES[0][0])
    params = models.TextField(null=True, blank=True)  # JSON


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ('name', 'room', 'index', 'type', 'params')

# TODO: sessions, and sessions records (rule, action, alarm, message, record)
