# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20150506_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_type', models.CharField(help_text=b'Whether the author of the feedback is the client or the freelancer.', max_length=2, choices=[(b'CL', b'Client'), (b'FR', b'Freelancer')])),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('booking', models.ForeignKey(to='booking.Booking')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
