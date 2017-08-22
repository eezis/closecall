# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0032_auto_20170822_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='ee_show_youtube_vid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='show_youtube_vid',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='youtube_offensive_votes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
