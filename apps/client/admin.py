from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export import resources, fields
from . import models


class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created')


class ClientResource(resources.ModelResource):
    "Import/export resource to allow exporting of client data."
    reference_number = fields.Field(column_name='Client reference',
                                    attribute='reference_number')
    last_name = fields.Field(column_name='Last name',
                                attribute='last_name')
    first_name = fields.Field(column_name='First name',
                                attribute='first_name')
    company_name = fields.Field(column_name='Company name',
                                attribute='company_name')
    user__email = fields.Field(column_name='Email',
                                attribute='user__email')
    mobile = fields.Field(column_name='Mobile',
                                attribute='mobile')

    class Meta:
        model = models.Client
        fields = ('reference_number',
                  'last_name', 'first_name',
                  'company_name', 'user__email', 'mobile')
        export_order = fields


class ClientAdmin(ExportActionModelAdmin):
    list_display = ('first_name', 'last_name', 'user',
                    'company_name', 'mobile')
    raw_id_fields = ('user',)
    search_fields = ('first_name', 'last_name',
                     'user__email')
    resource_class = ClientResource


admin.site.register(models.Lead, LeadAdmin)
admin.site.register(models.Client, ClientAdmin)
