# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='days_available',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=27, verbose_name=b'Which days of the week are you available to work?', choices=[(b'mon', b'Monday'), (b'tue', b'Tuesday'), (b'wed', b'Wednesday'), (b'thu', b'Thursday'), (b'fri', b'Friday'), (b'sat', b'Saturday'), (b'sun', b'Sunday')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='hours_available',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=11, verbose_name=b'What are your preferred working hours?', choices=[(b'MO', b'Mornings'), (b'AF', b'Afternoons'), (b'EV', b'Evenings'), (b'NI', b'Night')]),
            preserve_default=True,
        ),
    ]
