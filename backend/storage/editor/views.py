from rest_framework.decorators import api_view
from rest_framework.response import Response

from editor.models import Function, FunctionTemplateLink
from editor.models import ComponentTemplate, ComponentTemplateLink
from editor.models import Variable, VariableType
from editor.models import Rule, Component, ComponentArgument


def get_serialized_functions():
    functions = []
    for f in Function.objects.all():
        serialized_function = {
            'category': f.category,
            'return_type': f.return_type,
            'name': f.name,
            'links': [],
        }
        for ftl in FunctionTemplateLink.objects.filter(function=f):
            function_template_link = {
                'type': ftl.type,
            }
            if ftl.type == 'text':
                function_template_link['text'] = ftl.text
            elif ftl.type == 'argument':
                function_template_link['key'] = ftl.key
                function_template_link['default_value'] = ftl.default_value
            serialized_function['links'].append(function_template_link)
        functions.append(serialized_function)

    return functions


def get_serialized_component_templates(context):
    component_templates = []
    for ct in ComponentTemplate.objects.filter(context=context):
        component_template = {
            'name': ct.name,
            'links': [],
        }
        for ctl in ComponentTemplateLink.objects.filter(template=ct):
            component_template_link = {
                'type': ctl.type,
            }
            if ctl.type == 'text':
                component_template_link['text'] = ctl.text
            elif ctl.type == 'argument':
                component_template_link['key'] = ctl.key
                component_template_link['default_value'] = ctl.default_value
            component_template['links'].append(component_template_link)

        component_templates.append(component_template)

    return component_templates


@api_view(['GET'])
def get_templates(request):
    response = {
        'function': get_serialized_functions(),
        'trigger': get_serialized_component_templates('trigger'),
        'condition': get_serialized_component_templates('condition'),
        'action': get_serialized_component_templates('action'),
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


def get_serialized_components(rule, context):
    components = []
    for c in Component.objects.filter(rule=rule, template__context=context):
        component = {
            'id': c.id,
            'template': c.template.name,
            'arguments': {},
        }
        for ca in ComponentArgument.objects.filter(context=c):
            component[ca.key] = ca.value
        components.append(component)

    return components


def get_serialized_rules():
    rules = []
    for r in Rule.objects.all():
        rule = {
            'id': r.id,
            'name': r.name,
            'triggers': get_serialized_components(r, 'trigger'),
            'conditions': get_serialized_components(r, 'condition'),
            'actions': get_serialized_components(r, 'action'),
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
