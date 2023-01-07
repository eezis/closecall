# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0024_auto_20150126_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='accepted',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='reviewed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='witnesses',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Your Name and Names of other Witnesses ( this field is not published )', blank=True),
            preserve_default=True,
        ),
    ]
