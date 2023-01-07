# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0028_auto_20151027_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='warned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='warned_note',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
