from django.core.management.base import BaseCommand

from scenario.models import Room
from live.models import Card, CardRow


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id_in', type=int)
        parser.add_argument('id_out', type=int)

    def handle(self, *args, **options):
        id_in = options['id_in']
        id_out = options['id_out']

        room_in = Room.objects.get(id=id_in)
        room_out = Room.objects.get(id=id_out)

        Card.objects.filter(room=room_out).delete()

        cards_in = Card.objects.filter(room=room_in)
        for card in cards_in:
            card_rows_in = CardRow.objects.filter(card=card)

            card.pk = None
            card.room = room_out
            card.save()

            for card_row in card_rows_in:
                card_row.pk = None
                card_row.card = card
                card_row.save()
