from rest_framework.serializers import ModelSerializer, ValidationError

from editor.models import RuleSet


class RuleSetSerializer(ModelSerializer):
    class Meta:
        model = RuleSet
        fields = (
            'id',
            'name',
            'index',
            'rooms',
        )
