# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_invitation_date_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='date_declined',
            field=models.DateTimeField(help_text=b'When the freelancer was declined for the job.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
