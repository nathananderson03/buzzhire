# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def copy_driving_experience_old(apps, schema_editor):
    "Copy the old driving experience data to the new field."
    Driver = apps.get_model('driver', 'Driver')
    MAP = {
        '0-1': 0,
        '1-3': 1,
        '3-5': 3,
        '5+': 5,
    }
    for old, new in MAP.items():
        Driver.objects.filter(
                driving_experience_old=old).update(driving_experience=new)


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0005_auto_20150408_1529'),
    ]

    operations = [
        migrations.RunPython(copy_driving_experience_old),
    ]
