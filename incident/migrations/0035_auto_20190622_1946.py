# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0034_auto_20170904_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='vehicle_description',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Vehicle Description -- please fill this out!', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='video_embed_string',
            field=models.TextField(max_length=180, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='video_offensive_votes',
            field=models.IntegerField(default=0, verbose_name=b'Offensive'),
            preserve_default=True,
        ),
    ]
