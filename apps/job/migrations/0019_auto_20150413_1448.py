# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0018_jobrequest_phone_requirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='city',
            field=models.CharField(default=b'L', help_text=b'We currently only accept bookings in London.', max_length=1, blank=True, choices=[(b'L', b'London')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='comments',
            field=models.TextField(help_text=b'Anything else to tell the driver.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='number_of_freelancers',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Number of drivers required', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='pay_per_hour',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), help_text=b'How much you will pay per hour, for each driver.', max_digits=5, decimal_places=2, default_currency=b'GBP'),
            preserve_default=True,
        ),
    ]
