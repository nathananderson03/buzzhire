# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators
import djmoney.models.fields
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0031_auto_20150420_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='client_pay_per_hour',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('8'), max_digits=5, validators=[django.core.validators.MinValueValidator(8.0)], help_text=b'How much you will pay per hour, for each driver.', verbose_name=b'Pay per hour', default_currency=b'GBP'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='status',
            field=django_fsm.FSMField(default=b'OP', max_length=2, choices=[(b'OP', b'Open'), (b'CF', b'Confirmed'), (b'CP', b'Complete'), (b'CA', b'Cancelled')]),
            preserve_default=True,
        ),
    ]
