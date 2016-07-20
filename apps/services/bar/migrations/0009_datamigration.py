# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    BarPayGrade = apps.get_model('bar', 'BarPayGrade')
    # If there are no pay grades already, create some
    if not BarPayGrade.objects.exists():
        # Pay, years experience, role
        ITEMS = (
            (8.25, 0, 'BM'),
            (8.50, 3, 'BM'),
            (8.00, 0, 'BT'),
            (8.25, 3, 'BT'),
            (9.00, 0, 'MX'),
            (9.50, 3, 'MX'),
        )
        for min_client_pay_per_hour, years_experience, role in ITEMS:
            BarPayGrade.objects.create(
                min_client_pay_per_hour=min_client_pay_per_hour,
                min_client_pay_per_hour_currency='GBP',
                years_experience=years_experience,
                role=role)
            print 'Created bar pay grade.'


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0008_auto_20150821_1506'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
