from django.contrib import admin

from scenario.models import Scenario, ScenarioForm
from scenario.models import Room, RoomForm
from scenario.models import Camera, CameraForm


class ScenarioAdmin(admin.ModelAdmin):
    form = ScenarioForm
    list_display = ('name',)
    search_fields = ('name',)


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm
    list_display = (
        'scenario',
        'cardinal',
        'channel',
    )
    search_fields = (
        'scenario__name',
        'cardinal',
        'channel',
    )


class CameraAdmin(admin.ModelAdmin):
    form = CameraForm
    list_display = (
        'name',
        'url',
        'room',
    )
    search_fields = (
        'name',
        'url',
        'room__scenario__name',
        'room__cardinal',
    )


admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Camera, CameraAdmin)
