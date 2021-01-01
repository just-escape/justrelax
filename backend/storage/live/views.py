from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from editor.models import RuleSet
from live.models import Card, CardRow
from live.serializers import CardSerializer, CardRowSerializer


class CardView(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filterset_fields = ('room',)
    ordering_fields = ('index',)
    ordering = ('index',)


class CardRowView(ModelViewSet):
    queryset = CardRow.objects.all()
    serializer_class = CardRowSerializer
    filterset_fields = ('card',)
    ordering_fields = ('index',)
    ordering = ('index',)


def get_serialized_cards(rule_set):
    cards = []
    for c in Card.objects.filter(rule_set=rule_set).order_by('index'):
        card = {
            'id': c.id,
            'name': c.name,
            'index': c.index,
        }
        cards.append(card)
    return cards


@api_view(['GET'])
def get_cards_from_room_id(request):
    response = []

    room_id = int(request.GET.get('room_id'))

    rule_sets = RuleSet.objects.filter(rooms__id=room_id).order_by('index')
    for rs in rule_sets:
        response.extend(get_serialized_cards(rs))

    return Response(response)
