# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_auto_20150417_0940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcode',
            options={'ordering': ['postcode']},
        ),
        migrations.AddField(
            model_name='postcode',
            name='postcode',
            field=models.CharField(max_length=8, blank=True),
            preserve_default=True,
        ),
    ]
