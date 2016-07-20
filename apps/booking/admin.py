from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export import resources, fields
from apps.job.models import JobRequest
from apps.freelancer.admin import FreelancerAdmin
from apps.freelancer.models import Freelancer
from . import models

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest',
                    'date_created', 'date_applied', 'date_declined', 'manual')
    search_fields = ('freelancer__first_name', 'freelancer__last_name',
                     'freelancer__user__email')
    raw_id_fields = ('jobrequest', 'freelancer')
    readonly_fields = ('date_created', 'date_applied', 'date_declined')
    list_filter = ('manual',)
    exclude = ('date_accepted',)

admin.site.register(models.Invitation, InvitationAdmin)


class BookingResource(resources.ModelResource):
    "Import/export resource to allow exporting of booking data."

    booking_reference = fields.Field(column_name='Booking reference',
                                     attribute='reference_number')

    jobrequest_reference = fields.Field(column_name='Job reference')
    def dehydrate_jobrequest_reference(self, obj):
        return obj.jobrequest.reference_number

    service = fields.Field(column_name='Service')
    def dehydrate_service(self, obj):
        # Get polymorphic model
        polymorphic_job_request = JobRequest.objects.get(id=obj.jobrequest.id)
        return polymorphic_job_request.service

    client_name = fields.Field(column_name='Client name')
    def dehydrate_client_name(self, obj):
        return obj.jobrequest.client.get_full_name()

    date_created = fields.Field(column_name='Date booked',
                                attribute='date_created')

    jobrequest__date = fields.Field(column_name='Job date',
                                attribute='jobrequest__date')

    jobrequest__start_time = fields.Field(column_name='Job start time',
                                attribute='jobrequest__start_time')

    jobrequest__duration = fields.Field(column_name='Job duration (hours)',
                                attribute='jobrequest__duration')

    client_pay_per_hour = fields.Field(column_name='Client pay/hr (GBP)')
    def dehydrate_client_pay_per_hour(self, obj):
        return obj.jobrequest.client_pay_per_hour.amount

    freelancer_pay_per_hour = fields.Field(column_name='Freelancer pay/hr (GBP)')
    def dehydrate_freelancer_pay_per_hour(self, obj):
        return obj.jobrequest.freelancer_pay_per_hour.amount

    client_total_cost = fields.Field(column_name='Client total cost (GBP)')
    def dehydrate_client_total_cost(self, obj):
        return obj.jobrequest.client_total_cost.amount

    job_status = fields.Field(column_name='Job status')
    def dehydrate_job_status(self, obj):
        return obj.jobrequest.get_status_display()

    freelancer_name = fields.Field(column_name='Freelancer name')
    def dehydrate_freelancer_name(self, obj):
        return obj.freelancer.get_full_name()

    class Meta:
        model = models.Booking
        fields = ('booking_reference', 'jobrequest_reference', 'service',
                  'client_name', 'date_created',
                  'jobrequest__date', 'jobrequest__start_time',
                  'jobrequest__duration',
                  'client_pay_per_hour',
                  'freelancer_pay_per_hour',
                  'client_total_cost',
                  'job_status',
                  'freelancer_name')
        export_order = fields

class BookingAdmin(ExportActionModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest',
                    'date_created')
    search_fields = ('freelancer__first_name', 'freelancer__last_name',
                     'freelancer__user__email')
    raw_id_fields = ('jobrequest', 'freelancer')
    resource_class = BookingResource

admin.site.register(models.Booking, BookingAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('freelancer',)


admin.site.register(models.Availability, AvailabilityAdmin)


class AvailabilityInline(admin.StackedInline):
    model = models.Availability
    verbose_name_plural = "Availability"


# [MONKEY-PATCH] Once we need more than one inline within the freelancer admin,
#                we'll need to create an app that will register admins imbued
#                with dependent inlines.
#                Horrible explanation.
class AvailabilityFreelancerAdmin(FreelancerAdmin):
    inlines = FreelancerAdmin.inlines + [AvailabilityInline]


admin.site.unregister(Freelancer)
admin.site.register(Freelancer, AvailabilityFreelancerAdmin)
