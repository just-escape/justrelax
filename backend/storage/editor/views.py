from rest_framework.decorators import api_view
from rest_framework.response import Response

from editor.models import Function, FunctionLink, ContentType, ContentTypeLink
from editor.models import Variable, VariableType, Rule, Context, ContextArgument


def get_serialized_functions():
    functions = []
    for f in Function.objects.all():
        serialized_function = {
            'category': f.category,
            'return_type': f.return_type,
            'name': f.name,
            'links': [],
        }
        for fl in FunctionLink.objects.filter(function=f):
            function_link = {
                'link_type': fl.link_type,
            }
            if fl.link_type == 'text':
                function_link['text'] = fl.text
            elif fl.link_type == 'argument':
                function_link['key'] = fl.key
                function_link['default_value'] = fl.default_value
            serialized_function['links'].append(function_link)
        functions.append(serialized_function)

    return functions


def get_serialized_content_types(context_type):
    content_types = []
    for ct in ContentType.objects.filter(context_type=context_type):
        content_type = {
            'name': ct.name,
            'links': [],
        }
        for ctl in ContentTypeLink.objects.filter(content_type=ct):
            content_type_link = {
                'link_type': ctl.link_type,
            }
            if ctl.link_type == 'text':
                content_type_link['text'] = ctl.text
            elif ctl.link_type == 'argument':
                content_type_link['key'] = ctl.key
                content_type_link['default_value'] = ctl.default_value
            content_type['links'].append(content_type_link)

        content_types.append(content_type)

    return content_types


@api_view(['GET'])
def get_fixtures(request):
    response = {
        'functions': get_serialized_functions(),
        'trigger_types': get_serialized_content_types('trigger'),
        'condition_types': get_serialized_content_types('condition'),
        'action_types': get_serialized_content_types('action'),
    }

    return Response(response)


def get_serialized_variables():
    variables = []
    for v in Variable.objects.all():
        variable = {
            'id': v.id,
            'name': v.name,
            'init_value': v.init_value,
            'list': v.list,
            'types': [],
        }
        for vt in VariableType.objects.filter(variable=v):
            variable['types'].append(vt.type)
        variables.append(variable)

    return variables


def get_serialized_contexts(rule, context_type):
    contexts = []
    for c in Context.objects.filter(rule=rule, content_type__context_type=context_type):
        context = {
            'id': c.id,
            'content_type': c.content_type.name,
            'arguments': {},
        }
        for ca in ContextArgument.objects.filter(context=c):
            context[ca.key] = ca.value
        contexts.append(context)

    return contexts


def get_serialized_rules():
    rules = []
    for r in Rule.objects.all():
        rule = {
            'id': r.id,
            'name': r.name,
            'triggers': get_serialized_contexts(r, 'trigger'),
            'conditions': get_serialized_contexts(r, 'conditions'),
            'actions': get_serialized_contexts(r, 'actions'),
        }
        rules.append(rule)
    return rules


@api_view(['GET'])
def get_scenario(request):
    # scenario_id = int(request.GET.get('scenario_id'))

    response = {
        'variables': get_serialized_variables(),
        'rules': get_serialized_rules(),
    }

    return Response(response)
