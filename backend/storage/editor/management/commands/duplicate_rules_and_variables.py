from django.core.management.base import BaseCommand

from scenario.models import Room
from editor.models import Rule, Variable


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id_in', type=int)
        parser.add_argument('id_out', type=int)

    def handle(self, *args, **options):
        id_in = options['id_in']
        id_out = options['id_out']

        room_in = Room.objects.get(id=id_in)
        room_out = Room.objects.get(id=id_out)

        rules_in = Rule.objects.filter(room=room_in)
        variables_in = Variable.objects.filter(room=room_in)

        Rule.objects.filter(room=room_out).delete()
        Variable.objects.filter(room=room_out).delete()

        for rule in rules_in:
            rule.pk = None
            rule.room = room_out
            rule.save()

        for variable in variables_in:
            variable.pk = None
            variable.room = room_out
            variable.save()
