# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0038_auto_20150512_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_type',
            field=models.ForeignKey(related_name='jobrequests', blank=True, to='driver.FlexibleVehicleType', help_text=b'Which type of vehicle would be appropriate for the job. ', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='status',
            field=django_fsm.FSMField(default=b'IC', protected=True, max_length=2, choices=[(b'OP', b'Open'), (b'CF', b'Confirmed'), (b'CP', b'Complete'), (b'IC', b'In checkout'), (b'CA', b'Cancelled')]),
            preserve_default=True,
        ),
    ]
