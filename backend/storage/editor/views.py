import json

from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response

from scenario.models import Room
from editor.models import Template, TemplateLink, Variable, Rule, CONTEXTS


def get_serialized_templates():
    templates = []
    for t in Template.objects.all().order_by('index'):
        template = {
            'category': t.category,
            'name': t.name,
            'context': t.context,
            'links': [],
        }
        for link in TemplateLink.objects.filter(template=t).order_by('index'):
            template_link = {
                'type': link.type,
            }
            if link.type == 'text':
                template_link['locale'] = link.locale
            elif link.type == 'argument':
                template_link['key'] = link.key
                template_link['default_value'] = link.default_value
                template_link['value_type'] = link.value_type
                if link.predefined_choices:
                    template_link['predefined_choices'] = link.predefined_choices.split(',')
                else:
                    template_link['predefined_choices'] = None
            template['links'].append(template_link)

        templates.append(template)

    return templates


@api_view(['GET'])
def get_templates(request):
    response = get_serialized_templates()
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


def get_serialized_rules(room):
    rules = []
    for r in Rule.objects.filter(room=room).order_by('index'):
        rule = {
            'id': r.id,
            'name': r.name,
            'content': json.loads(r.content),
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

                json_content = json.dumps(rule['content'])
                if rule_to_update.content != json_content:
                    rule_to_update.content = json_content
                    save = True

                if save:
                    rule_to_update.save()

    # Create
    for rule_index, rule in enumerate(rules):
        if rule.get('id', None) not in ids_to_update:
            new_rule = Rule(
                room=room,
                name=rule['name'],
                index=rule_index,
                content=json.dumps(rule['content']),
            )
            new_rule.save()


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
