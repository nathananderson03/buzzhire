# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20150408_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='jobrequest',
            field=models.ForeignKey(related_name='bookings', to='job.JobRequest'),
            preserve_default=True,
        ),
    ]
