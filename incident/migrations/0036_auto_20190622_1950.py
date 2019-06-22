# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0035_auto_20190622_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='video_embed_string',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
