# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0002_setup_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='barfreelancer',
            name='role',
            field=models.CharField(default=b'BM', max_length=2, choices=[(b'BM', b'Barman'), (b'MX', b'Mixologist'), (b'BT', b'Barista')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barjobrequest',
            name='role',
            field=models.CharField(default=b'BM', max_length=2, choices=[(b'BM', b'Barman'), (b'MX', b'Mixologist'), (b'BT', b'Barista')]),
            preserve_default=True,
        ),
    ]
