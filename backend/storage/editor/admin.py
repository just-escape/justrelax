from django.contrib import admin

from editor.models import Function, FunctionForm
from editor.models import FunctionTemplateLink, FunctionTemplateLinkForm
from editor.models import Variable, VariableForm
from editor.models import Rule, RuleForm
from editor.models import ComponentTemplate, ComponentTemplateForm
from editor.models import ComponentTemplateLink, ComponentTemplateLinkForm
from editor.models import Component, ComponentForm
from editor.models import ComponentArgument, ComponentArgumentForm


class FunctionAdmin(admin.ModelAdmin):
    form = FunctionForm
    list_display = ('category', 'index', 'name', 'return_type',)
    search_fields = ('category', 'name', 'return_type',)


class FunctionTemplateLinkAdmin(admin.ModelAdmin):
    form = FunctionTemplateLinkForm
    list_display = (
        'function',
        'index',
        'type',
        'text',
        'key',
        'value_type',
        'default_value',
        'predefined_choices',
    )
    search_fields = (
        'function__name',
        'type',
        'text',
        'key',
        'default_value',
    )


class VariableAdmin(admin.ModelAdmin):
    form = VariableForm
    list_display = ('room', 'index', 'name', 'type', 'init_value', 'list',)
    search_fields = ('name', 'type', 'init_value', 'list',)


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm
    list_display = ('room', 'index', 'name',)
    search_fields = ('name',)


class ComponentTemplateAdmin(admin.ModelAdmin):
    form = ComponentTemplateForm
    list_display = ('index', 'name', 'context',)
    search_fields = ('name', 'context',)


class ComponentTemplateLinkAdmin(admin.ModelAdmin):
    form = ComponentTemplateLinkForm
    list_display = (
        'template',
        'index',
        'type',
        'text',
        'key',
        'value_type',
        'default_value',
        'predefined_choices',
    )
    search_fields = (
        'template__name',
        'type',
        'text',
        'key',
        'default_value',
    )


class ComponentAdmin(admin.ModelAdmin):
    form = ComponentForm
    list_display = (
        'rule',
        'template',
        'index',
    )
    search_fields = (
        'rule__name',
        'template__context_type',
    )


class ComponentArgumentAdmin(admin.ModelAdmin):
    form = ComponentArgumentForm
    list_display = (
        'component',
        'key',
        'value',
    )
    search_fields = (
        'component__rule__name',
        'component__template__name',
        'component__template__context',
        'key',
        'value',
    )


admin.site.register(Function, FunctionAdmin)
admin.site.register(FunctionTemplateLink, FunctionTemplateLinkAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(ComponentTemplate, ComponentTemplateAdmin)
admin.site.register(ComponentTemplateLink, ComponentTemplateLinkAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(ComponentArgument, ComponentArgumentAdmin)
