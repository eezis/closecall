# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0002_incident_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='position',
        ),
    ]
