from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin
from . import models

# This is necessary just to allow search_fields to work elsewhere
class JobRequestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'duration', 'end_datetime', 'postcode')
    list_filter = ('status', 'date',)
    search_fields = ('id',)
    date_hierarchy = 'date'
    fsm_field = ['status']
    exclude = ('status', 'phone_requirement_old')
    readonly_fields = ['status_display', 'end_datetime']
    raw_id_fields = ('client',)

    def status_display(self, instance):
        return instance.get_status_display()
    status_display.short_description = 'Status'

admin.site.register(models.JobRequest, JobRequestAdmin)
