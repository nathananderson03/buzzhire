# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    CleanerPayGrade = apps.get_model('cleaner', 'CleanerPayGrade')
    # If there are no pay grades already, create some
    if not CleanerPayGrade.objects.exists():
        # Pay, years experience, role
        ITEMS = (
            (8.50, 0),
            (8.50, 3),
        )
        for min_client_pay_per_hour, years_experience in ITEMS:
            CleanerPayGrade.objects.create(
                min_client_pay_per_hour=min_client_pay_per_hour,
                min_client_pay_per_hour_currency='GBP',
                years_experience=years_experience)
            print 'Created cleaner pay grade.'

class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0007_datamigration'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
