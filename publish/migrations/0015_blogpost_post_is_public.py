# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0014_auto_20141221_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='post_is_public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
