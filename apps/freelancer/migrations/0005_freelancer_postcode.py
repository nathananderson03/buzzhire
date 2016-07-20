# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('freelancer', '0004_auto_20150416_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='postcode',
            field=models.ForeignKey(blank=True, to='location.Postcode', null=True),
            preserve_default=True,
        ),
    ]
