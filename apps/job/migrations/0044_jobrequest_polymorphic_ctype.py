# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('job', '0043_move_driverjobrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_job.jobrequest_set+', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
