# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_setup_perms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='motorcycle_licence',
            field=models.BooleanField(default=False, verbose_name=b'I have a CBT/full motorcycle license.'),
            preserve_default=True,
        ),
    ]
