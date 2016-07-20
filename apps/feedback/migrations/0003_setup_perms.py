# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def datamigration(apps, schema_editor):
    "Adds ability for site admin to create, edit and delete feedback."
    add_admin_perms(apps.get_model('feedback', 'BookingFeedback'))


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_bookingfeedback_comment'),
    ]

    operations = [
        migrations.RunPython(datamigration),
    ]
