# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    """Adds ability for site admin to create, edit and delete invitations.
    """
    Invitation = apps.get_model('booking', 'Invitation')
    add_admin_perms(Invitation)

class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20150612_1507'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
