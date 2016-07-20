# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    """Adds ability for site admin to create, edit and delete freelancers.
    """
    Freelancer = apps.get_model('freelancer', 'Freelancer')
    add_admin_perms(Freelancer)

class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0002_auto_20150331_1543'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
