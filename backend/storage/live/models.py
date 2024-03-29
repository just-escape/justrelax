from django.db import models
from django import forms

from editor.models import RuleSet


class Card(models.Model):
    rule_set = models.ForeignKey(RuleSet, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    index = models.IntegerField()

    def __str__(self):
        return str(self.name)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('rule_set', 'name', 'index',)


class CardRow(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    index = models.IntegerField()
    maintenance = models.BooleanField(default=False)
    widget = models.CharField(max_length=32)
    widget_params = models.TextField()

    def __str__(self):
        return str(self.name)


class CardRowForm(forms.ModelForm):
    class Meta:
        model = CardRow
        fields = ('card', 'name', 'index', 'maintenance', 'widget', 'widget_params',)
