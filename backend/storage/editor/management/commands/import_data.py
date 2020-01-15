from django.core.management.base import BaseCommand

from editor.models import Function, FunctionTemplateLink
from editor.models import ComponentTemplate, ComponentTemplateLink
from editor.models import Variable, VariableType
from editor.models import Rule, Component, ComponentArgument


FUNCTIONS = [
    {
        'category': 'arithmetic',
        'index': 1,
        'name': '+',
        'return_type': 'integer',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': 1,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' + ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': 1,
            },
        ],
    },
    {
        'category': 'arithmetic',
        'index': 2,
        'name': '-',
        'return_type': 'integer',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': 1,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' - ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': 1,
            },
        ],
    },
    {
        'category': 'arithmetic',
        'index': 3,
        'name': '*',
        'return_type': 'integer',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': 1,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' * ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': 1,
            },
        ],
    },
    {
        'category': 'arithmetic',
        'index': 4,
        'name': '/',
        'return_type': 'integer',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': 1,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' / ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': 1,
            },
        ],
    },
]

COMPONENT_TEMPLATES = [
    {
        'index': 1000,
        'name': 'incoming_event',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'An event has been received',
            },
        ],
    },
    {
        'index': 1001,
        'name': 'session_tick',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Each session tick',
            },
        ],
    },
    {
        'index': 1002,
        'name': 'session_start',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'The session has started',
            },
        ],
    },
    {
        'index': 1003,
        'name': 'session_pause',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'The session has paused',
            },
        ],
    },
    {
        'index': 1004,
        'name': 'session_resume',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'The session has resumed',
            },
        ],
    },
    {
        'index': 2000,
        'name': 'simple_condition',
        'context': 'condition',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'If ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'condition',
                'default_value': True,
            },
        ],
    },
    {
        'index': 2001,
        'name': 'or',
        'context': 'condition',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': True,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' or ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': True,
            },
        ],
    },
    {
        'index': 2002,
        'name': 'and',
        'context': 'condition',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': True,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' and ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': True,
            },
        ],
    },
    {
        'index': 3000,
        'name': 'send_event',
        'context': 'action',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Send event ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'event',
                'default_value': 'hello',
            },
            {
                'index': 3,
                'type': 'text',
                'text': ' to node named ',
            },
            {
                'index': 4,
                'type': 'argument',
                'key': 'node_name',
                'default_value': 'node',
            },
        ],
    },
    {
        'index': 3001,
        'name': 'set_variable',
        'context': 'action',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Set variable ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'variable_name',
                'default_value': 'variable',
            },
            {
                'index': 3,
                'type': 'text',
                'text': ' to value ',
            },
            {
                'index': 4,
                'type': 'argument',
                'key': 'value',
                'default_value': 'value',
            },
        ],
    },
    {
        'index': 3002,
        'name': 'trigger_rule',
        'context': 'action',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Trigger rule named ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'rule_name',
                'default_value': 'rule',
            },
        ],
    },
]

VARIABLES = [
    {
        'index': 1,
        'name': 'variable',
        'init_value': None,
        'list': False,
        'types': ['boolean', 'integer', 'real', 'string', 'object'],
    },
    {
        'index': 2,
        'name': 'variable2',
        'init_value': None,
        'list': False,
        'types': ['boolean', 'integer', 'real', 'string', 'object'],
    },
]


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
