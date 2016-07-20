# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    "Save all the JobRequests, so that an end datetime is auto-generated."
    # Loading JobRequest using apps.get_model doesn't trigger the save()
    # method, so we need to import directly
    from ..models import JobRequest
    try:
        [j.save() for j in JobRequest.objects.all()]
    except:
        print 'Did not successfully resave all JobRequests - skipping.'
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0040_jobrequest_end_datetime'),
    ]

    operations = [
        migrations.RunPython(datamigration, lambda x, y: False)
    ]
