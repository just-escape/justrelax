from django.core.management.base import BaseCommand

from scenario.models import Room
from editor.models import Template, TemplateLink, Variable, Rule

from editor.management.commands.template_fixtures import TEMPLATES
from editor.management.commands.variable_fixtures import VARIABLES


class Command(BaseCommand):
    def handle(self, *args, **options):
        Template.objects.all().delete()

        Variable.objects.all().delete()
        Rule.objects.all().delete()

        for t_index, t in enumerate(TEMPLATES):
            created_template = Template.objects.create(
                category=t['category'],
                index=t_index,
                name=t['name'],
                context=t['context'],
            )
            for link_index, link in enumerate(t['links']):
                TemplateLink.objects.create(
                    template=created_template,
                    index=link_index,
                    type=link['type'],
                    locale=link.get('locale', None),
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
