# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0007_auto_20141126_0025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incident',
            options={'ordering': ['created'], 'verbose_name': 'Incident', 'verbose_name_plural': 'Incidents'},
        ),
    ]
