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

TEMPLATE_LINK_TYPES = (
    ('text', 'text'),
    ('argument', 'argument'),
)


class Function(models.Model):
    category = models.CharField(max_length=64, blank=True)
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=64, unique=True)
    return_type = models.CharField(
        choices=VALUE_TYPES, default=VALUE_TYPES[0][0], max_length=8)


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
    text = models.CharField(max_length=128, null=True)

    # relevant if type is argument
    key = models.CharField(max_length=64, null=True)
    default_value = models.TextField(null=True, blank=True)

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


class FunctionTemplateLinkForm(forms.ModelForm):
    class Meta:
        model = FunctionTemplateLink
        fields = (
            'function',
            'index',
            'type',
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
    text = models.CharField(max_length=128, null=True)

    # relevant if type is argument
    key = models.CharField(max_length=64, null=True)
    default_value = models.TextField(null=True, blank=True)

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


class ComponentTemplateLinkForm(forms.ModelForm):
    class Meta:
        model = ComponentTemplateLink
        fields = (
            'template',
            'index',
            'type',
            'text',
            'key',
            'default_value',
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


class ComponentArgumentForm(forms.ModelForm):
    class Meta:
        model = ComponentArgument
        fields = (
            'component',
            'key',
            'value',
        )
