# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('freelancer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='freelancer.Freelancer')),
                ('vehicle_types', multiselectfield.db.fields.MultiSelectField(max_length=11, choices=[(b'BI', b'Bicycle'), (b'MC', b'Motorcycle/scooter'), (b'CA', b'Car'), (b'VA', b'Van')])),
                ('motorcycle_licence', models.BooleanField(default=False, help_text=b'If you are a motorcycle/scooter driver, do you have yourCBT/full motorcycle license? ')),
                ('driving_experience', models.CharField(max_length=3, choices=[(b'0-1', b'Less than 1 year'), (b'1-3', b'1 - 3 years'), (b'3-5', b'3 - 5 year'), (b'5+', b'More than 5 years')])),
                ('own_vehicle', models.BooleanField(default=False, verbose_name=b'I have my own vehicle')),
            ],
            options={
            },
            bases=('freelancer.freelancer',),
        ),
    ]
