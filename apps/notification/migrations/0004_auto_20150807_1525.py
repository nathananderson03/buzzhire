# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20150714_1547'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-datetime_created',)},
        ),
        migrations.AddField(
            model_name='notification',
            name='datetime_deleted',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
