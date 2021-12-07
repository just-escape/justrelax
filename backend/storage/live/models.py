from django.db import models
from django import forms

from editor.models import RuleSet


WIDGET_TYPES = (
    ('buttons_group', 'buttons_group'),
    ('session_data', 'session_data'),
    ('log_prompt', 'log_prompt'),
    ('instruction_prompt', 'instruction_prompt'),
    ('lasers', 'lasers'),
    ('waffle_factory', 'waffle_factory'),
    ('synchronizer_lights', 'synchronizer_lights'),
    ('textarea', 'textarea'),
    ('node_register', 'node_register'),
)


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
    widget = models.CharField(choices=WIDGET_TYPES, default=WIDGET_TYPES[0][0], max_length=32)
    widget_params = models.TextField()

    def __str__(self):
        return str(self.name)


class CardRowForm(forms.ModelForm):
    class Meta:
        model = CardRow
        fields = ('card', 'name', 'index', 'widget', 'widget_params',)
