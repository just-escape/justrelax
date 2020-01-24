from django.core.management.base import BaseCommand

from scenario.models import Room
from editor.models import Function, FunctionTemplateLink
from editor.models import ComponentTemplate, ComponentTemplateLink
from editor.models import Variable
from editor.models import Rule, Component

from editor.management.commands.f_fixtures import FUNCTIONS
from editor.management.commands.ct_fixtures import COMPONENT_TEMPLATES
from editor.management.commands.v_fixtures import VARIABLES


class Command(BaseCommand):
    def handle(self, *args, **options):
        Function.objects.all().delete()
        ComponentTemplate.objects.all().delete()

        Variable.objects.all().delete()
        Rule.objects.all().delete()

        for f_index, f in enumerate(FUNCTIONS):
            created_function = Function.objects.create(
                category=f['category'],
                index=f_index,
                name=f['name'],
                return_type=f['return_type'],
            )
            for link_index, link in enumerate(f['links']):
                FunctionTemplateLink.objects.create(
                    function=created_function,
                    index=link_index,
                    type=link['type'],
                    text=link.get('text', None),
                    key=link.get('key', None),
                    value_type=link.get('value_type', 'string'),
                    predefined_choices=link.get('predefined_choices', ''),
                    default_value=link.get('default_value', None),
                )

        for ct_index, ct in enumerate(COMPONENT_TEMPLATES):
            created_component_template = ComponentTemplate.objects.create(
                context=ct['context'],
                index=ct_index,
                name=ct['name'],
            )
            for link_index, link in enumerate(ct['links']):
                ComponentTemplateLink.objects.create(
                    template=created_component_template,
                    index=link_index,
                    type=link['type'],
                    text=link.get('text', None),
                    key=link.get('key', None),
                    value_type=link.get('value_type', 'string'),
                    predefined_choices=link.get('predefined_choices', ''),
                    default_value=link.get('default_value', None),
                )

        r = Room.objects.get(id=1)
        for v_index, v in enumerate(VARIABLES):
            Variable.objects.create(
                room=r,
                index=v_index,
                name=v['name'],
                init_value=v['init_value'],
                list=v['list'],
                type=v['type'],
            )

        Component.objects.all().delete()
