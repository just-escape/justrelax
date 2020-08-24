from django.db import models
from django import forms

from scenario.models import Room


WIDGET_TYPES = (
    ('buttons_group', 'buttons_group'),
)


class Card(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    index = models.IntegerField()

    def __str__(self):
        return str(self.name)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('room', 'name', 'index',)


class CardRow(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    index = models.IntegerField()
    widget = models.CharField(choices=WIDGET_TYPES, default=WIDGET_TYPES[0][0], max_length=32)
    widget_params = models.TextField()

    def __str__(self):
        return str(self.name)


class CardRowForm(forms.ModelForm):
    class Meta:
        model = CardRow
        fields = ('card', 'name', 'index', 'widget', 'widget_params',)
