from django.contrib import admin

from editor.models import Function, FunctionForm
from editor.models import FunctionLink, FunctionLinkForm
from editor.models import Variable, VariableForm
from editor.models import VariableType, VariableTypeForm
from editor.models import Rule, RuleForm
from editor.models import ContentType, ContentTypeForm
from editor.models import ContentTypeLink, ContentTypeLinkForm
from editor.models import Context, ContextForm
from editor.models import ContextValue, ContextValueForm


class FunctionAdmin(admin.ModelAdmin):
    form = FunctionForm
    list_display = ('category', 'index', 'name', 'return_type',)
    search_fields = ('category', 'name', 'return_type',)


class FunctionLinkAdmin(admin.ModelAdmin):
    form = FunctionLinkForm
    list_display = (
        'function',
        'index',
        'link_type',
        'text',
        'key',
        'default_value',
    )
    search_fields = (
        'function__name',
        'link_type',
        'text',
        'key',
        'default_value',
    )


class VariableAdmin(admin.ModelAdmin):
    form = VariableForm
    list_display = ('s', 'index', 'name', 'init_value', 'list',)
    search_fields = ('s', 'name', 'init_value', 'list',)


class VariableTypeAdmin(admin.ModelAdmin):
    form = VariableTypeForm
    list_display = ('variable', 'type',)
    search_fields = ('variable__name', 'type',)


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm
    list_display = ('s', 'index', 'name',)
    search_fields = ('s', 'name',)


class ContentTypeAdmin(admin.ModelAdmin):
    form = ContentTypeForm
    list_display = ('index', 'name', 'context_type',)
    search_fields = ('name', 'context_type',)


class ContentTypeLinkAdmin(admin.ModelAdmin):
    form = ContentTypeLinkForm
    list_display = (
        'content_type',
        'index',
        'link_type',
        'text',
        'key',
        'default_value',
    )
    search_fields = (
        'content_type__name',
        'link_type',
        'text',
        'key',
        'default_value',
    )


class ContextAdmin(admin.ModelAdmin):
    form = ContextForm
    list_display = (
        'rule',
        'content_type',
        'index',
    )
    search_fields = (
        'rule__name',
        'content_type__context_type',
    )


class ContextValueAdmin(admin.ModelAdmin):
    form = ContextValueForm
    list_display = (
        'context',
        'key',
        'value',
    )
    search_fields = (
        'context__rule__name',
        'context__rule__content_type__context_type',
        'key',
        'value',
    )


admin.site.register(Function, FunctionAdmin)
admin.site.register(FunctionLink, FunctionLinkAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(VariableType, VariableTypeAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(ContentTypeLink, ContentTypeLinkAdmin)
admin.site.register(Context, ContextAdmin)
admin.site.register(ContextValue, ContextValueAdmin)
