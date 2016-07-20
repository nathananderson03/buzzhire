# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db import connection

def set_ctype(apps, schema_editor):
    """Populates the ctype field for existing job requests
    (they will all be drivers)."""
    try:
        ContentType = apps.get_model('contenttypes', 'ContentType')
        content_type_pk = ContentType.objects.get(app_label='driver',
                                                  model='driverjobrequest').pk
        # We have to do this with raw SQL as the model manager is broken until we
        # do this.
        cursor = connection.cursor()
        cursor.execute("UPDATE job_jobrequest SET polymorphic_ctype_id = %s",
                       [content_type_pk])
    except:
        # For later installations, this will fail, because driverjobrequests no longer exist
        print('Skipping setting ctype for driver job requests.')

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0044_jobrequest_polymorphic_ctype'),
    ]

    operations = [
        migrations.RunPython(set_ctype)
    ]
