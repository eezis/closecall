# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0029_auto_20151027_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='latitude',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='longitude',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
