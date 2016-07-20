# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_invitation_manual'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='created',
            new_name='date_created',
        ),
    ]
