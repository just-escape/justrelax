import json

from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from editor.models import Template, TemplateLink, TemplateContextParagraph, Variable, Rule
from editor.models import RuleSet
from editor.serializers import RuleSetSerializer


class RuleSetView(ModelViewSet):
    queryset = RuleSet.objects.all()
    serializer_class = RuleSetSerializer
    ordering_fields = ('index',)
    ordering = ('index',)


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

        cps = TemplateContextParagraph.objects.filter(template=t).order_by('index')
        if cps:
            template['context_paragraphs'] = []
            for cp in cps:
                context_paragraph = {
                    'type': cp.type,
                    'key': cp.key,
                }
                template['context_paragraphs'].append(context_paragraph)

        templates.append(template)

    return templates


@api_view(['GET'])
def get_templates(request):
    response = get_serialized_templates()
    return Response(response)


def get_serialized_variables(rule_set):
    variables = []
    for v in Variable.objects.filter(rule_set=rule_set).order_by('index'):
        variable = {
            'id': v.id,
            'name': v.name,
            'type': v.type,
            'init_value': v.init_value,
            'list': v.list,
        }
        variables.append(variable)

    return variables


def get_serialized_rules(rule_set):
    rules = []
    for r in Rule.objects.filter(rule_set=rule_set).order_by('index'):
        rule = {
            'id': r.id,
            'name': r.name,
            'content': json.loads(r.content),
        }
        rules.append(rule)
    return rules


@api_view(['GET'])
def get_rules_from_room_id(request):
    response = []

    room_id = int(request.GET.get('room_id'))

    rule_sets = RuleSet.objects.filter(rooms__id=room_id).order_by('index')
    for rs in rule_sets:
        response.append(
            {
                'ruleset_id': rs.id,
                'rules': get_serialized_rules(rs),
                'variables': get_serialized_variables(rs),
            }
        )

    return Response(response)


@api_view(['GET'])
def get_rules_from_rule_set_id(request):
    id_ = int(request.GET.get('id'))

    rule_set = RuleSet.objects.get(id=id_)
    response = {
        'rules': get_serialized_rules(rule_set),
        'variables': get_serialized_variables(rule_set),
    }

    return Response(response)


def update_rules(rule_set, rules):
    rule_ids = {r.get('id', None) for r in rules}
    rule_ids.discard(None)

    old_rules = Rule.objects.filter(rule_set=rule_set)
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
                rule_set=rule_set,
                name=rule['name'],
                index=rule_index,
                content=json.dumps(rule['content']),
            )
            new_rule.save()


def update_variables(rule_set, variables):
    variable_ids = {v.get('id', None) for v in variables}
    variable_ids.discard(None)

    old_variables = Variable.objects.filter(rule_set=rule_set)
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
                rule_set=rule_set,
                name=v['name'],
                index=index,
                init_value=v['init_value'],
                list=v['list'],
            )
            new_variable.save()


@api_view(['POST'])
def update_rule_set(request):
    rule_set_id = int(request.POST.get('rule_set_id'))
    rules = json.loads(request.POST.get('rules'))
    variables = json.loads(request.POST.get('variables'))

    with transaction.atomic():
        rule_set = RuleSet.objects.get(id=rule_set_id)

        update_rules(rule_set, rules)
        update_variables(rule_set, variables)

        response = {
            'variables': get_serialized_variables(rule_set),
            'rules': get_serialized_rules(rule_set),
        }

    return Response(response)
