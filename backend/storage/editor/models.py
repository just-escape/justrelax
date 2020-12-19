from django.db import models
from django import forms

from scenario.models import Room


CATEGORIES = (
    ('', ''),
    ('event', 'event'),
    ('admin', 'admin'),
    ('time', 'time'),
    ('session', 'session'),
    ('object', 'object'),
    ('conversion', 'conversion'),
    ('timer', 'timer'),
    ('math', 'math'),
    ('trigger', 'trigger'),
)

VALUE_TYPES = (
    ('string', 'string'),
    ('boolean', 'boolean'),
    ('integer', 'integer'),
    ('real', 'real'),
    ('object', 'object'),
    ('predefined', 'predefined'),
    ('variable', 'variable'),
    ('timer', 'timer'),
    ('disabled', 'disabled'),  # Special behavior on the interface
)

CONTEXTS = (
    ('trigger', 'trigger'),
    ('condition', 'condition'),
    ('action', 'action'),
    ('string', 'string'),
    ('boolean', 'boolean'),
    ('integer', 'integer'),
    ('real', 'real'),
    ('object', 'object'),
    ('timer', 'timer'),
)

PARAGRAPH_TYPES = (
    ('trigger', 'trigger'),
    ('condition', 'condition'),
    ('action', 'action'),
)

TEMPLATE_LINK_TYPES = (
    ('text', 'text'),
    ('argument', 'argument'),
)


class Template(models.Model):
    category = models.CharField(
        choices=CATEGORIES, default=CATEGORIES[0][0],
        max_length=64, blank=True)
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=64, unique=True)
    context = models.CharField(
        choices=CONTEXTS, default=CONTEXTS[0][0], max_length=16)

    def __str__(self):
        return self.name


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('category', 'index', 'name', 'context',)


class TemplateLink(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    index = models.IntegerField()
    type = models.CharField(
        max_length=16,
        choices=TEMPLATE_LINK_TYPES,
        default=TEMPLATE_LINK_TYPES[0][0],
    )

    # relevant if type is text
    locale = models.CharField(max_length=128, null=True, blank=True)

    # relevant if type is argument
    key = models.CharField(max_length=64, null=True)
    value_type = models.CharField(choices=VALUE_TYPES, max_length=16, default=VALUE_TYPES[0][0])
    default_value = models.TextField(null=True, blank=True)
    predefined_choices = models.TextField(null=True, blank=True)  # comma-separated values

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['template', 'key'],
                name='template_key',
            )
        ]

    def __str__(self):
        return '{} template ({})'.format(self.template.name, self.index)


class TemplateLinkForm(forms.ModelForm):
    class Meta:
        model = TemplateLink
        fields = (
            'template',
            'index',
            'type',
            'locale',
            'key',
            'value_type',
            'default_value',
            'predefined_choices',
        )


class TemplateContextParagraph(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    index = models.IntegerField()
    key = models.CharField(max_length=64, null=False, blank=False)
    type = models.CharField(
        choices=PARAGRAPH_TYPES, default=PARAGRAPH_TYPES[0][0], max_length=16)

    def __str__(self):
        return '{} template ({})'.format(self.template.name, self.index)


class TemplateContextParagraphForm(forms.ModelForm):
    class Meta:
        model = TemplateContextParagraph
        fields = (
            'template',
            'index',
            'key',
            'type',
        )


class RuleSet(models.Model):
    name = models.CharField(max_length=64)
    index = models.IntegerField()
    rooms = models.ManyToManyField(Room)


class RuleSetForm(forms.ModelForm):
    class Meta:
        model = RuleSet
        fields = ('name', 'index', 'rooms')


class Variable(models.Model):
    rule_set = models.ForeignKey(RuleSet, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=64)
    type = models.CharField(choices=VALUE_TYPES, default=VALUE_TYPES[0][0], max_length=16)
    init_value = models.TextField(null=True, blank=True)
    list = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.room, self.name)


class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ('rule_set', 'index', 'name', 'type', 'init_value', 'list',)


class Rule(models.Model):
    rule_set = models.ForeignKey(RuleSet, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return '{} - {}'.format(self.room, self.name)


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ('rule_set', 'index', 'name', 'content')
