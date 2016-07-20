# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0046_auto_20150618_1445'),
        ('freelancer', '0013_auto_20150618_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingFreelancer',
            fields=[
                ('freelancer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='freelancer.Freelancer')),
            ],
            options={
                'abstract': False,
            },
            bases=('freelancer.freelancer',),
        ),
        migrations.CreateModel(
            name='WaitingJobRequest',
            fields=[
                ('jobrequest_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='job.JobRequest')),
            ],
            options={
                'abstract': False,
            },
            bases=('job.jobrequest',),
        ),
    ]
