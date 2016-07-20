# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0002_auto_20150331_1543'),
        ('job', '0008_auto_20150402_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(related_name='bookings', to='freelancer.Freelancer')),
                ('jobrequest', models.ForeignKey(related_name='jobrequests', to='job.JobRequest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set([('freelancer', 'jobrequest')]),
        ),
    ]
