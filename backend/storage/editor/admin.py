from django.contrib import admin

from editor.models import Template, TemplateForm
from editor.models import TemplateLink, TemplateLinkForm
from editor.models import TemplateContextParagraph, TemplateContextParagraphForm
from editor.models import RuleSet, RuleSetForm
from editor.models import Variable, VariableForm
from editor.models import Rule, RuleForm


class TemplateAdmin(admin.ModelAdmin):
    form = TemplateForm
    list_display = ('category', 'index', 'name', 'context',)
    search_fields = ('category', 'name', 'context',)


class TemplateLinkAdmin(admin.ModelAdmin):
    form = TemplateLinkForm
    list_display = (
        'template',
        'index',
        'type',
        'locale',
        'key',
        'value_type',
        'default_value',
        'predefined_choices',
    )
    search_fields = (
        'template__name',
        'type',
        'locale',
        'key',
        'default_value',
    )


class TemplateContextParagraphAdmin(admin.ModelAdmin):
    form = TemplateContextParagraphForm
    list_display = (
        'template',
        'index',
        'key',
        'type',
    )
    search_fields = (
        'template__name',
        'index',
        'key',
        'type',
    )


class VariableAdmin(admin.ModelAdmin):
    form = VariableForm
    list_display = ('rule_set', 'index', 'name', 'type', 'init_value', 'list',)
    search_fields = ('name', 'type', 'init_value', 'list',)


class RuleSetAdmin(admin.ModelAdmin):
    form = RuleSetForm
    list_display = ('index', 'name')
    search_fields = ('index', 'name')


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm
    list_display = ('rule_set', 'index', 'name', 'content',)
    search_fields = ('name', 'content',)


admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateLink, TemplateLinkAdmin)
admin.site.register(TemplateContextParagraph, TemplateContextParagraphAdmin)
admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Rule, RuleAdmin)
