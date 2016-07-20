# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverJobRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'OP', max_length=2, choices=[(b'OP', b'Open'), (b'CF', b'Confirmed'), (b'CP', b'Complete'), (b'CA', b'Cancelled')])),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('number_of_freelancers', models.PositiveSmallIntegerField(default=1, null=True, verbose_name=b'Number of interpreters required', blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('vehicle_types', multiselectfield.db.fields.MultiSelectField(max_length=11, choices=[(b'BI', b'Bicycle'), (b'MC', b'Motorcycle/scooter'), (b'CA', b'Car'), (b'VA', b'Van')])),
                ('driving_experience', models.CharField(max_length=3, choices=[(b'0-1', b'Less than 1 year'), (b'1-3', b'1 - 3 years'), (b'3-5', b'3 - 5 year'), (b'5+', b'More than 5 years')])),
                ('client', models.ForeignKey(related_name='job_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_submitted',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
