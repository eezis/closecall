# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0005_auto_20141120_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='location',
        ),
        migrations.AddField(
            model_name='incident',
            name='address',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
