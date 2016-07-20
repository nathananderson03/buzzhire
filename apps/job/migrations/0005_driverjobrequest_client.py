# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_client_perms'),
        ('job', '0004_remove_driverjobrequest_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='client',
            field=models.ForeignKey(related_name='job_requests', default=1, to='client.Client'),
            preserve_default=False,
        ),
    ]
