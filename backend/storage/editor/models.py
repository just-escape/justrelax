from django.db import models
from django import forms

# from scenario.models import Scenario


VALUE_TYPES = (
    ('boolean', 'boolean'),
    ('integer', 'integer'),
    ('real', 'real'),
    ('string', 'string'),
    ('object', 'object'),
)

STRUCTURE_LINK_TYPES = (
    ('text', 'text'),
    ('value', 'value'),
)


class Function(models.Model):
    category = models.CharField(max_length=64)
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    return_type = models.CharField(
        choices=VALUE_TYPES, default=VALUE_TYPES[0][0], max_length=8)


class FunctionForm(forms.ModelForm):
    class Meta:
        model = Function
        fields = ('category', 'index', 'name',)


class FunctionLink(models.Model):
    function = models.ForeignKey(Function, on_delete=models.CASCADE)

    index = models.IntegerField()
    link_type = models.CharField(
        max_length=16,
        choices=STRUCTURE_LINK_TYPES,
        default=STRUCTURE_LINK_TYPES[0][0],
    )

    # relevant if link_type is text
    text = models.CharField(max_length=128, null=True)

    # relevant if link_type is value
    key = models.CharField(max_length=64, null=True, unique=True)
    default_value = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['function', 'index'],
                name='function_link_index',
            ),
        ]


class FunctionLinkForm(forms.ModelForm):
    class Meta:
        model = FunctionLink
        fields = (
            'function',
            'index',
            'link_type',
            'text',
            'key',
            'default_value',
        )


class Variable(models.Model):
    # scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    s = models.CharField(max_length=64, default="s1")
    index = models.IntegerField()
    name = models.CharField(max_length=64)
    init_value = models.TextField(null=True, blank=True)
    list = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['s', 'index'],
                name='variable_index',
            ),
            models.UniqueConstraint(
                fields=['s', 'name'],
                name='variable_name',
            ),
        ]


class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ('s', 'index', 'name', 'init_value', 'list',)


class VariableType(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    type = models.CharField(
        choices=VALUE_TYPES, default=VALUE_TYPES[0][0], max_length=8)


class VariableTypeForm(forms.ModelForm):
    class Meta:
        model = VariableType
        fields = ('variable', 'type',)


class Rule(models.Model):
    # scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    s = models.CharField(max_length=64, default="s1")
    index = models.IntegerField()
    name = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['s', 'index'], name='rule_index'),
        ]


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ('s', 'index', 'name',)


class ContentType(models.Model):
    CONTEXT_TYPES = (
        ('trigger', 'trigger'),
        ('condition', 'condition'),
        ('action', 'action'),
    )

    index = models.IntegerField()
    name = models.CharField(max_length=64)
    context_type = models.CharField(
        max_length=16, choices=CONTEXT_TYPES, default=CONTEXT_TYPES[0][0])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['context_type', 'index'],
                name='content_type_index',
            ),
        ]


class ContentTypeForm(forms.ModelForm):
    class Meta:
        model = ContentType
        fields = ('index', 'name', 'context_type',)


class ContentTypeLink(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    index = models.IntegerField()
    link_type = models.CharField(
        max_length=16,
        choices=STRUCTURE_LINK_TYPES,
        default=STRUCTURE_LINK_TYPES[0][0],
    )

    # relevant if link_type is text
    text = models.CharField(max_length=128, null=True)

    # relevant if link_type is value
    key = models.CharField(max_length=64, null=True, unique=True)
    default_value = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'index'],
                name='content_type_link_index',
            ),
        ]


class ContentTypeLinkForm(forms.ModelForm):
    class Meta:
        model = ContentTypeLink
        fields = (
            'content_type',
            'index',
            'link_type',
            'text',
            'key',
            'default_value',
        )


class Context(models.Model):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    index = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rule', 'index'],
                name='context_index',
            ),
        ]


class ContextForm(forms.ModelForm):
    class Meta:
        model = Context
        fields = (
            'rule',
            'content_type',
            'index',
        )


class ContextValue(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, null=True)
    value = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['context', 'key'],
                name='content_value_key',
            ),
        ]


class ContextValueForm(forms.ModelForm):
    class Meta:
        model = ContextValue
        fields = (
            'context',
            'key',
            'value',
        )
