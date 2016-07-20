# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0011_auto_20150528_1021'),
        ('job', '0042_auto_20150604_1755'),
        ('booking', '0005_auto_20150506_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_accepted', models.DateTimeField(null=True, blank=True)),
                ('freelancer', models.ForeignKey(related_name='invitations', to='freelancer.Freelancer')),
                ('jobrequest', models.ForeignKey(related_name='invitations', to='job.JobRequest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('freelancer', 'jobrequest')]),
        ),
    ]
