from django.contrib import admin

from session.models import Session, SessionForm
from session.models import Record, RecordForm


class SessionAdmin(admin.ModelAdmin):
    form = SessionForm
    list_display = ('room', 'start_date', 'end_date', 'duration',)


class RecordAdmin(admin.ModelAdmin):
    form = RecordForm
    list_display = ('session', 'label', 'date', 'moment',)
    search_fields = ('label',)


admin.site.register(Session, SessionAdmin)
admin.site.register(Record, RecordAdmin)
