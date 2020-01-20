from django.core.management.base import BaseCommand

from editor.models import Function, FunctionTemplateLink
from editor.models import ComponentTemplate, ComponentTemplateLink
from editor.models import Variable, VariableType
from editor.models import Rule, Component, ComponentArgument

from editor.management.commands.f_fixtures import FUNCTIONS
from editor.management.commands.ct_fixtures import COMPONENT_TEMPLATES
from editor.management.commands.v_fixtures import VARIABLES


class Command(BaseCommand):
    def handle(self, *args, **options):
        Function.objects.all().delete()
        ComponentTemplate.objects.all().delete()

        Variable.objects.all().delete()
        Rule.objects.all().delete()

        for f in FUNCTIONS:
            created_function = Function.objects.create(
                category=f['category'],
                index=f['index'],
                name=f['name'],
                return_type=f['return_type'],
            )
            for link in f['links']:
                FunctionTemplateLink.objects.create(
                    function=created_function,
                    index=link['index'],
                    type=link['type'],
                    text=link.get('text', None),
                    key=link.get('key', None),
                    default_value=link.get('default_value', None),
                )

        for ct in COMPONENT_TEMPLATES:
            created_component_template = ComponentTemplate.objects.create(
                context=ct['context'],
                index=ct['index'],
                name=ct['name'],
            )
            for link in ct['links']:
                ComponentTemplateLink.objects.create(
                    template=created_component_template,
                    index=link['index'],
                    type=link['type'],
                    text=link.get('text', None),
                    key=link.get('key', None),
                    default_value=link.get('default_value', None),
                )

        for v in VARIABLES:
            created_variable = Variable.objects.create(
                index=v['index'],
                name=v['name'],
                init_value=v['init_value'],
                list=v['list'],
            )
            for v_type in v['types']:
                VariableType.objects.create(
                    variable=created_variable,
                    type=v_type,
                )

        Component
        ComponentArgument
