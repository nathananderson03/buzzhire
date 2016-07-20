# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20150612_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='manual',
            field=models.BooleanField(default=True, help_text=b'Whether this invitation was created manually.'),
            preserve_default=True,
        ),
    ]
