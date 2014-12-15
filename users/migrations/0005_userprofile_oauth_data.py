# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20141214_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='oauth_data',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
