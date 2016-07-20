# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0003_setup_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='minimum_pay_per_hour',
            field=djmoney.models.fields.MoneyField(default=Decimal('8.5'), help_text=b'The minimum pay per hour you will accept.', max_digits=5, decimal_places=2, default_currency=b'GBP'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='freelancer',
            name='minimum_pay_per_hour_currency',
            field=djmoney.models.fields.CurrencyField(default=b'GBP', max_length=3, editable=False, choices=[(b'GBP', 'Pound Sterling')]),
            preserve_default=True,
        ),
    ]
