from django.contrib import admin

from scenario.models import Scenario, ScenarioForm
from scenario.models import Room, RoomForm
from scenario.models import Camera, CameraForm


class ScenarioAdmin(admin.ModelAdmin):
    form = ScenarioForm
    list_display = ('index', 'name',)
    search_fields = ('name',)


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm
    list_display = (
        'index',
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
        'index',
        'name',
        'room',
        'type',
        'params',
    )
    search_fields = (
        'name',
        'params',
        'type',
        'room__scenario__name',
        'room__cardinal',
    )


admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Camera, CameraAdmin)
