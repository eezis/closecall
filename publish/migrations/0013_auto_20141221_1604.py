# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0012_auto_20141221_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(unique=True, max_length=120),
            preserve_default=True,
        ),
    ]
