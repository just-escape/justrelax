from django.db import models
from django import forms


class Scenario(models.Model):
    name = models.CharField(max_length=64)


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ('name',)


class Room(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    cardinal = models.CharField(max_length=16, null=True, blank=True)
    channel = models.CharField(max_length=64)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('scenario', 'cardinal', 'channel',)


class Camera(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ('name', 'url', 'room',)

# TODO: sessions, and sessions records (rule, action, alarm, message, record)
