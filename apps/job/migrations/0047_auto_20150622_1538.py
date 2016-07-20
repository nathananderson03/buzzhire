# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0046_auto_20150618_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='client_pay_per_hour',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('8'), max_digits=5, validators=[django.core.validators.MinValueValidator(8.0)], help_text=b'How much you will pay per hour, for each freelancer.', verbose_name=b'Pay per hour', default_currency=b'GBP'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='comments',
            field=models.TextField(help_text=b'Anything else to tell the freelancer.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='phone_requirement',
            field=models.CharField(default=b'NR', help_text=b'Whether the freelancer needs a smart phone to do this job (for example, if you need them to run an app).', max_length=2, choices=[(b'NR', b'No smart phone needed'), (b'AY', b'Any smart phone'), (b'AN', b'Android'), (b'IP', b'iPhone'), (b'WI', b'Windows')]),
            preserve_default=True,
        ),
    ]
