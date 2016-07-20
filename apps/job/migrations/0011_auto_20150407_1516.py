# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_jobrequest_postcode_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='postcode_area',
            field=models.CharField(max_length=2, verbose_name=b'Location', choices=[(b'C', b'Central London (Postcodes: EC, WC)'), (b'W', b'West London (Postcodes: W)'), (b'SW', b'South West London (Postcodes: SW)'), (b'SE', b'South East London (Postcodes: SE)'), (b'E', b'East London (Postcodes: E)'), (b'N', b'North London (Postcodes: N)'), (b'NW', b'North West London (Postcodes: NW)')]),
            preserve_default=True,
        ),
    ]
