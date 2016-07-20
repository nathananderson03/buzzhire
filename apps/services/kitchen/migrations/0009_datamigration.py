# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    KitchenPayGrade = apps.get_model('kitchen', 'KitchenPayGrade')
    # If there are no pay grades already, create some
    if not KitchenPayGrade.objects.exists():
        # Pay, years experience, role
        ITEMS = (
            (8.00, 0, 'PO'),
            (8.25, 3, 'PO'),
            (8.25, 0, 'KA'),
            (8.50, 3, 'KA'),
            (8.50, 0, 'CH'),
            (8.75, 3, 'CH'),
        )
        for min_client_pay_per_hour, years_experience, role in ITEMS:
            KitchenPayGrade.objects.create(
                min_client_pay_per_hour=min_client_pay_per_hour,
                min_client_pay_per_hour_currency='GBP',
                years_experience=years_experience,
                role=role)
            print 'Created kitchen pay grade.'

class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0008_auto_20150821_1506'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
