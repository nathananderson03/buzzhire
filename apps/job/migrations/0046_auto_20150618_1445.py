# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0045_set_ctype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='number_of_freelancers',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Number of freelancers required', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
    ]
