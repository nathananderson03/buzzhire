# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    "Adds ability for site admin to create, edit and delete clients."
    Lead = apps.get_model('client', 'Client')
    add_admin_perms(Lead)

class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20150331_1543'),
    ]

    operations = [
        migrations.RunPython(setup_perms),
    ]
