from django.contrib import admin

from live.models import Card, CardForm
from live.models import CardRow, CardRowForm


class CardAdmin(admin.ModelAdmin):
    form = CardForm
    list_display = ('room', 'name', 'index',)
    search_fields = ('room', 'name',)


class CardRowAdmin(admin.ModelAdmin):
    form = CardRowForm
    list_display = ('card', 'name', 'index', 'widget', 'widget_params',)


admin.site.register(Card, CardAdmin)
admin.site.register(CardRow, CardRowAdmin)
