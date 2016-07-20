# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0015_jobrequest_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrequest',
            name='postcode_area',
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='address1',
            field=models.CharField(default='1 Test Road', max_length=75, verbose_name=b'Address line 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='address2',
            field=models.CharField(max_length=75, verbose_name=b'Address line 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='postcode',
            field=models.CharField(default='SW1A 1AA', max_length=10),
            preserve_default=False,
        ),
    ]
