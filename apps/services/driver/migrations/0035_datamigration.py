# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    # Go through all the driver job requests and set the legacy
    # phone requirement field (which is on the JobRequest model)
    # to the new phone requirement field.
    DriverJobRequest = apps.get_model('driver', 'DriverJobRequest')
    for job_request in DriverJobRequest.objects.all():
        job_request.phone_requirement = job_request.phone_requirement_old
        job_request.save()

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0034_driverjobrequest_phone_requirement'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
