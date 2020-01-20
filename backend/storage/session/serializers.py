from rest_framework.serializers import ModelSerializer

from session.models import Session, Record


class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = (
            'id',
            'start_date',
            'end_date',
            'duration',
        )


class RecordSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = (
            'id',
            'session',
            'label',
            'date',
            'moment',
        )
