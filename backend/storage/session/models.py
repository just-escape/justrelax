from django.db import models
from django import forms

from scenario.models import Room


class Session(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DurationField()


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('room', 'start_date', 'end_date', 'duration',)


class Record(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
    date = models.DateTimeField()
    moment = models.DurationField()


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('session', 'label', 'date', 'moment',)
