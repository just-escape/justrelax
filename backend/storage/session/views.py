from rest_framework.viewsets import ModelViewSet

from session.models import Session, Record
from session.serializers import SessionSerializer, RecordSerializer


class SessionView(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filterset_fields = ('room',)


class RecordView(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_fields = ('session',)
