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


class Camera(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    index = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'index'],
                name='room_index',
            ),
        ]


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ('name', 'url', 'room', 'index',)

# TODO: sessions, and sessions records (rule, action, alarm, message, record)
