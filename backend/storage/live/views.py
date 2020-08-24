from rest_framework.viewsets import ModelViewSet

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
