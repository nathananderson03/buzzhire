# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0025_driverjobrequest_minimum_delivery_box'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobrequest',
            old_name='pay_per_hour',
            new_name='client_pay_per_hour',
        ),
        migrations.RenameField(
            model_name='jobrequest',
            old_name='pay_per_hour_currency',
            new_name='client_pay_per_hour_currency',
        ),
    ]
