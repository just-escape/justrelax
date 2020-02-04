import json

from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response

from scenario.models import Room
from editor.models import Function, FunctionTemplateLink
from editor.models import ComponentTemplate, ComponentTemplateLink
from editor.models import Variable
from editor.models import Rule, Component, ComponentArgument


def get_serialized_functions():
    functions = []
    for f in Function.objects.all().order_by('index'):
        serialized_function = {
            'category': f.category,
            'return_type': f.return_type,
            'name': f.name,
            'links': [],
        }
        for ftl in FunctionTemplateLink.objects.filter(function=f).order_by('index'):
            function_template_link = {
                'type': ftl.type,
            }
            if ftl.type == 'text':
                function_template_link['text'] = ftl.text
            elif ftl.type == 'argument':
                function_template_link['key'] = ftl.key
                function_template_link['default_value'] = ftl.default_value
                function_template_link['value_type'] = ftl.value_type
                if ftl.predefined_choices:
                    function_template_link['predefined_choices'] = ftl.predefined_choices.split(',')
                else:
                    function_template_link['predefined_choices'] = None
            serialized_function['links'].append(function_template_link)
        functions.append(serialized_function)

    return functions


def get_serialized_component_templates(context):
    component_templates = []
    for ct in ComponentTemplate.objects.filter(context=context).order_by('index'):
        component_template = {
            'name': ct.name,
            'links': [],
        }
        for ctl in ComponentTemplateLink.objects.filter(template=ct).order_by('index'):
            component_template_link = {
                'type': ctl.type,
            }
            if ctl.type == 'text':
                component_template_link['text'] = ctl.text
            elif ctl.type == 'argument':
                component_template_link['key'] = ctl.key
                component_template_link['default_value'] = ctl.default_value
                component_template_link['value_type'] = ctl.value_type
                if ctl.predefined_choices:
                    component_template_link['predefined_choices'] = ctl.predefined_choices.split(',')
                else:
                    component_template_link['predefined_choices'] = None
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


def get_serialized_variables(room):
    variables = []
    for v in Variable.objects.filter(room=room).order_by('index'):
        variable = {
            'id': v.id,
            'name': v.name,
            'type': v.type,
            'init_value': v.init_value,
            'list': v.list,
        }
        variables.append(variable)

    return variables


def get_serialized_components(rule, context):
    components = []
    for c in Component.objects.filter(rule=rule, template__context=context).order_by('index'):
        component = {
            'id': c.id,
            'template': c.template.name,
            'arguments': {},
        }
        for ca in ComponentArgument.objects.filter(component=c):
            component['arguments'][ca.key] = json.loads(ca.value)
        components.append(component)

    return components


def get_serialized_rules(room):
    rules = []
    for r in Rule.objects.filter(room=room).order_by('index'):
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
    room_id = int(request.GET.get('room_id'))
    room = Room.objects.get(id=room_id)

    response = {
        'variables': get_serialized_variables(room),
        'rules': get_serialized_rules(room),
    }

    return Response(response)


def create_component(rule, component, context, index):
    template = ComponentTemplate.objects.get(
        name=component['template'],
        context=context,
    )
    new_component = Component(
        rule=rule,
        template=template,
        index=index,
    )
    new_component.save()

    for key, value in component['arguments'].items():
        ComponentArgument(
            component=new_component,
            key=key,
            value=json.dumps(value),
        ).save()


def update_component_arguments(component, arguments):
    argument_keys = {*arguments.keys()}

    old_arguments = ComponentArgument.objects.filter(component=component)
    old_argument_keys = {a.key for a in old_arguments}

    # Delete
    keys_to_delete = old_argument_keys - argument_keys
    old_arguments.filter(key__in=keys_to_delete, component=component)

    # Update
    keys_to_update = argument_keys & old_argument_keys
    for key in keys_to_update:
        value = json.dumps(arguments[key])
        argument_to_update = ComponentArgument.objects.get(component=component, key=key)

        if argument_to_update.value != value:
            argument_to_update.value = value
            argument_to_update.save()

    # Create
    arguments_to_create = {key: value for key, value in arguments.items() if key not in keys_to_update}
    for key, value in arguments_to_create.items():
        ComponentArgument(
            component=component,
            key=key,
            value=json.dumps(value),
        ).save()


def update_components(rule, components, context):
    component_ids = {c.get('id', None) for c in components}
    component_ids.discard(None)

    old_components = Component.objects.all()
    old_component_ids = {c.id for c in old_components}

    # Delete
    ids_to_delete = old_component_ids - component_ids
    old_components.filter(id__in=ids_to_delete, rule=rule, template__context=context).delete()

    # Update
    ids_to_update = component_ids & old_component_ids
    for id_ in ids_to_update:
        save = False
        for index, component in enumerate(components):
            if component.get('id', None) == id_:
                component_to_update = Component.objects.get(id=id_)

                template = ComponentTemplate.objects.get(name=component['template'])
                if component_to_update.template != template:
                    component_to_update.template = template
                    save = True

                if component_to_update.index != index:
                    component_to_update.index = index
                    save = True

                if save:
                    component_to_update.save()

                # Update arguments
                update_component_arguments(component_to_update, component['arguments'])

    # Create
    for index, c in enumerate(components):
        if c.get('id', None) not in ids_to_update:
            create_component(rule, c, context, index)


def update_rules(room, rules):
    rule_ids = {r.get('id', None) for r in rules}
    rule_ids.discard(None)

    old_rules = Rule.objects.filter(room=room)
    old_rule_ids = {r.id for r in old_rules}

    # Delete
    ids_to_delete = old_rule_ids - rule_ids
    old_rules.filter(id__in=ids_to_delete).delete()

    # Update
    ids_to_update = rule_ids & old_rule_ids
    for id_ in ids_to_update:
        save = False
        for index, rule in enumerate(rules):
            if rule.get('id', None) == id_:
                rule_to_update = Rule.objects.get(id=id_)

                if rule_to_update.name != rule['name']:
                    rule_to_update.name = rule['name']
                    save = True

                if rule_to_update.index != index:
                    rule_to_update.index = index
                    save = True

                if save:
                    rule_to_update.save()

                # Update components
                update_components(rule_to_update, rule['triggers'], 'trigger')
                update_components(rule_to_update, rule['conditions'], 'condition')
                update_components(rule_to_update, rule['actions'], 'action')

    # Create
    for rule_index, rule in enumerate(rules):
        if rule.get('id', None) not in ids_to_update:
            new_rule = Rule(
                room=room,
                name=rule['name'],
                index=rule_index,
            )
            new_rule.save()

            for component_index, component in enumerate(rule['triggers']):
                create_component(
                    new_rule,
                    component,
                    'trigger',
                    component_index,
                )

            for component_index, component in enumerate(rule['conditions']):
                create_component(
                    new_rule,
                    component,
                    'condition',
                    component_index,
                )

            for component_index, component in enumerate(rule['actions']):
                create_component(
                    new_rule,
                    component,
                    'action',
                    component_index,
                )


def update_variables(room, variables):
    variable_ids = {v.get('id', None) for v in variables}
    variable_ids.discard(None)

    old_variables = Variable.objects.filter(room=room)
    old_variable_ids = {v.id for v in old_variables}

    # Delete
    ids_to_delete = old_variable_ids - variable_ids
    old_variables.filter(id__in=ids_to_delete).delete()

    # Update
    ids_to_update = variable_ids & old_variable_ids
    for id_ in ids_to_update:
        save = False
        for index, variable in enumerate(variables):
            if variable.get('id', None) == id_:
                variable_to_update = Variable.objects.get(id=id_)

                if variable_to_update.name != variable['name']:
                    variable_to_update.name = variable['name']
                    save = True

                if variable_to_update.type != variable['type']:
                    variable_to_update.type = variable['type']
                    save = True

                if variable_to_update.index != index:
                    variable_to_update.index = index
                    save = True

                if variable_to_update.init_value != variable['init_value']:
                    variable_to_update.init_value = variable['init_value']
                    save = True

                if variable_to_update.list != variable['list']:
                    variable_to_update.list = variable['list']
                    save = True

                if save:
                    variable_to_update.save()

    # Create
    for index, v in enumerate(variables):
        if v.get('id', None) not in ids_to_update:
            new_variable = Variable(
                room=room,
                name=v['name'],
                index=index,
                init_value=v['init_value'],
                list=v['list'],
            )
            new_variable.save()


@api_view(['POST'])
def update_scenario(request):
    room_id = int(request.POST.get('room_id'))
    rules = json.loads(request.POST.get('rules'))
    variables = json.loads(request.POST.get('variables'))

    with transaction.atomic():
        room = Room.objects.get(id=room_id)

        update_rules(room, rules)
        update_variables(room, variables)

        response = {
            'variables': get_serialized_variables(room),
            'rules': get_serialized_rules(room),
        }

    return Response(response)
