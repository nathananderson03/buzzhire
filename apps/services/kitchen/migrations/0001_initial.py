# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0048_jobrequest_years_experience'),
        ('freelancer', '0014_freelancer_years_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='KitchenFreelancer',
            fields=[
                ('freelancer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='freelancer.Freelancer')),
                ('certification', models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'Chef'), (b'SC', b'Sous chef'), (b'KA', b'Kitchen assistant'), (b'PO', b'Kitchen porter')])),
            ],
            options={
                'abstract': False,
            },
            bases=('freelancer.freelancer',),
        ),
        migrations.CreateModel(
            name='KitchenJobRequest',
            fields=[
                ('jobrequest_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='job.JobRequest')),
                ('certification', models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'Chef'), (b'SC', b'Sous chef'), (b'KA', b'Kitchen assistant'), (b'PO', b'Kitchen porter')])),
            ],
            options={
                'abstract': False,
            },
            bases=('job.jobrequest',),
        ),
    ]
