# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0002_setup_perms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kitchenfreelancer',
            name='certification',
        ),
        migrations.RemoveField(
            model_name='kitchenjobrequest',
            name='certification',
        ),
        migrations.AddField(
            model_name='kitchenfreelancer',
            name='role',
            field=models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'Chef'), (b'KA', b'Kitchen assistant'), (b'PO', b'Kitchen porter')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kitchenjobrequest',
            name='role',
            field=models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'Chef'), (b'KA', b'Kitchen assistant'), (b'PO', b'Kitchen porter')]),
            preserve_default=True,
        ),
    ]
