from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export import resources, fields
from apps.freelancer.templatetags.freelancer import profile_photo
from django.template.loader import render_to_string
from . import models

class FreelancerResource(resources.ModelResource):
    "Import/export resource to allow exporting of freelancer data."

    reference_number = fields.Field(column_name='Freelancer reference',
                                    attribute='reference_number')
    last_name = fields.Field(column_name='Last name',
                                attribute='last_name')
    first_name = fields.Field(column_name='First name',
                                attribute='first_name')
    user__email = fields.Field(column_name='Email',
                                attribute='user__email')
    mobile = fields.Field(column_name='Mobile',
                                attribute='mobile')

    service = fields.Field(column_name='Service',
                           attribute='service')

    published = fields.Field(column_name='Published',
                                attribute='published')

    class Meta:
        model = models.Freelancer
        fields = ('reference_number',
                  'last_name', 'first_name',
                  'user__email', 'mobile',
                  'service', 'published')
        export_order = fields


class FreelancerAdmin(ExportActionModelAdmin):
    def photo_display(self, obj):
        return render_to_string('freelancer/includes/profile_photo.html',
                                profile_photo(obj, 'small'))

    photo_display.short_description = 'Photo'
    photo_display.allow_tags = True

    list_display = ('photo_display', 'reference_number', 'user',
                    'first_name', 'last_name',
                    'published', 'postcode')
    list_filter = ('published',)
    search_fields = ('first_name', 'last_name', 'user__email')
    raw_id_fields = ('user',)
    resource_class = FreelancerResource

    exclude = ('days_available', 'hours_available')

admin.site.register(models.Freelancer, FreelancerAdmin)
