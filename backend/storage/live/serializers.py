import json

from rest_framework.serializers import ModelSerializer, ValidationError

from live.models import Card, CardRow


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'room',
            'name',
            'index',
        )


class CardRowSerializer(ModelSerializer):
    class Meta:
        model = CardRow
        fields = (
            'id',
            'card',
            'name',
            'index',
            'widget',
            'widget_params',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['widget_params'] = json.loads(ret['widget_params'])
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        try:
            ret['widget_params'] = json.dumps(ret['widget_params'])
        except TypeError:
            raise ValidationError(
                {
                    'widget_params': 'Value must be valid JSON.'
                }
            )

        return ret
