# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_setup_perms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcode',
            options={},
        ),
        migrations.RenameField(
            model_name='postcode',
            old_name='postcode',
            new_name='compressed_postcode',
        ),
    ]
