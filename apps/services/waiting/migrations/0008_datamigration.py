# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    WaitingPayGrade = apps.get_model('waiting', 'WaitingPayGrade')
    # If there are no pay grades already, create some
    if not WaitingPayGrade.objects.exists():
        # Pay, years experience
        ITEMS = (
            (8.00, 0),
            (8.25, 3),
        )
        for min_client_pay_per_hour, years_experience in ITEMS:
            WaitingPayGrade.objects.create(
                min_client_pay_per_hour=min_client_pay_per_hour,
                min_client_pay_per_hour_currency='GBP',
                years_experience=years_experience)
            print 'Created waiting pay grade.'

class Migration(migrations.Migration):

    dependencies = [
        ('waiting', '0007_auto_20150821_1506'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
