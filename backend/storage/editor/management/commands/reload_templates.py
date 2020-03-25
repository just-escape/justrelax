from django.core.management.base import BaseCommand

from editor.models import Template, TemplateLink, TemplateContextParagraph, Rule

from editor.management.commands.template_fixtures import TEMPLATES


class Command(BaseCommand):
    def handle(self, *args, **options):
        Template.objects.all().delete()

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

            context_paragraphs = t.get('context_paragraphs', [])
            for cp_index, cp in enumerate(context_paragraphs):
                TemplateContextParagraph.objects.create(
                    template=created_template,
                    index=cp_index,
                    key=cp['key'],
                    type=cp['type'],
                )
