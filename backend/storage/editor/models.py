from django.db import models
from django import forms

from scenario.models import Room


VALUE_TYPES = (
    ('string', 'string'),
    ('boolean', 'boolean'),
    ('integer', 'integer'),
    ('real', 'real'),
    ('object', 'object'),
    ('predefined', 'predefined'),
    ('variable', 'variable'),
    ('disabled', 'disabled'),  # Special behavior on the interface
)

TEMPLATE_LINK_TYPES = (
    ('text', 'text'),
    ('argument', 'argument'),
)


class Function(models.Model):
    category = models.CharField(max_length=64, blank=True)
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=64, unique=True)
    return_type = models.CharField(
        choices=VALUE_TYPES, default=VALUE_TYPES[0][0], max_length=16)

    def __str__(self):
        return self.name


class FunctionForm(forms.ModelForm):
    class Meta:
        model = Function
        fields = ('category', 'index', 'name', 'return_type',)


class FunctionTemplateLink(models.Model):
    function = models.ForeignKey(Function, on_delete=models.CASCADE)

    index = models.IntegerField()
    type = models.CharField(
        max_length=16,
        choices=TEMPLATE_LINK_TYPES,
        default=TEMPLATE_LINK_TYPES[0][0],
    )

    # relevant if type is text
    text = models.CharField(max_length=128, null=True, blank=True)

    # relevant if type is argument
    key = models.CharField(max_length=64, null=True)
    value_type = models.CharField(choices=VALUE_TYPES, max_length=16, default=VALUE_TYPES[0][0])
    default_value = models.TextField(null=True, blank=True)
    predefined_choices = models.TextField(null=True, blank=True)  # comma-separated values

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['function', 'index'],
                name='function_index',
            ),
            models.UniqueConstraint(
                fields=['function', 'key'],
                name='function_key',
            )
        ]

    def __str__(self):
        return '{} template ({})'.format(self.function.name, self.index)


class FunctionTemplateLinkForm(forms.ModelForm):
    class Meta:
        model = FunctionTemplateLink
        fields = (
            'function',
            'index',
            'type',
            'text',
            'key',
            'value_type',
            'default_value',
            'predefined_choices',
        )


class Variable(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=64)
    type = models.CharField(choices=VALUE_TYPES, default=VALUE_TYPES[0][0], max_length=16)
    init_value = models.TextField(null=True, blank=True)
    list = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'index'],
                name='variable_room_index',
            ),
            models.UniqueConstraint(
                fields=['room', 'name'],
                name='variable_room_name',
            ),
        ]

    def __str__(self):
        return '{} - {}'.format(self.room, self.name)


class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ('room', 'index', 'name', 'type', 'init_value', 'list',)


class Rule(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'index'], name='rule_room_index'),
        ]

    def __str__(self):
        return '{} - {}'.format(self.room, self.name)


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ('room', 'index', 'name',)


class ComponentTemplate(models.Model):
    CONTEXTS = (
        ('trigger', 'trigger'),
        ('condition', 'condition'),
        ('action', 'action'),
    )

    index = models.IntegerField()
    name = models.CharField(max_length=64)
    context = models.CharField(
        max_length=16, choices=CONTEXTS, default=CONTEXTS[0][0])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['context', 'index'],
                name='context_index',
            ),
            models.UniqueConstraint(
                fields=['context', 'name'],
                name='context_name',
            )
        ]

    def __str__(self):
        return '{} - {}'.format(self.context, self.name)


class ComponentTemplateForm(forms.ModelForm):
    class Meta:
        model = ComponentTemplate
        fields = ('index', 'name', 'context',)


class ComponentTemplateLink(models.Model):
    template = models.ForeignKey(ComponentTemplate, on_delete=models.CASCADE)

    index = models.IntegerField()
    type = models.CharField(
        max_length=16,
        choices=TEMPLATE_LINK_TYPES,
        default=TEMPLATE_LINK_TYPES[0][0],
    )

    # relevant if type is text
    text = models.CharField(max_length=128, null=True, blank=True)

    # relevant if type is argument
    key = models.CharField(max_length=64, null=True)
    value_type = models.CharField(choices=VALUE_TYPES, max_length=16, default=VALUE_TYPES[0][0])
    default_value = models.TextField(null=True, blank=True)
    predefined_choices = models.TextField(null=True, blank=True)  # comma-separated values

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['template', 'index'],
                name='template_index',
            ),
            models.UniqueConstraint(
                fields=['template', 'key'],
                name='template_key',
            )
        ]

    def __str__(self):
        return "{} template ({})".format(self.template, self.index)


class ComponentTemplateLinkForm(forms.ModelForm):
    class Meta:
        model = ComponentTemplateLink
        fields = (
            'template',
            'index',
            'type',
            'text',
            'key',
            'value_type',
            'default_value',
            'predefined_choices',
        )


class Component(models.Model):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    template = models.ForeignKey(ComponentTemplate, on_delete=models.CASCADE)
    index = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rule', 'template', 'index'],
                name='rule_template_index',
            ),
        ]

    def __str__(self):
        return "{} - {}".format(self.rule, self.template)


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = (
            'rule',
            'template',
            'index',
        )


class ComponentArgument(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, null=True)
    value = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['component', 'key'],
                name='component_key',
            ),
        ]

    def __str__(self):
        return "{} - {}={}".format(self.component, self.key, self.value)


class ComponentArgumentForm(forms.ModelForm):
    class Meta:
        model = ComponentArgument
        fields = (
            'component',
            'key',
            'value',
        )
