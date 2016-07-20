# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0032_auto_20150506_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='status',
            field=django_fsm.FSMField(default=b'IC', protected=True, max_length=2, choices=[(b'IC', b'In checkout'), (b'OP', b'Open'), (b'CF', b'Confirmed'), (b'CP', b'Complete'), (b'CA', b'Cancelled')]),
            preserve_default=True,
        ),
    ]
