# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0003_auto_20150625_1649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='barfreelancer',
            options={'verbose_name': 'bartender', 'verbose_name_plural': 'bar staff'},
        ),
        migrations.AlterField(
            model_name='barfreelancer',
            name='role',
            field=models.CharField(default=b'BM', max_length=2, choices=[(b'BM', b'Bartender'), (b'MX', b'Mixologist'), (b'BT', b'Barista')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='barjobrequest',
            name='role',
            field=models.CharField(default=b'BM', max_length=2, choices=[(b'BM', b'Bartender'), (b'MX', b'Mixologist'), (b'BT', b'Barista')]),
            preserve_default=True,
        ),
    ]
