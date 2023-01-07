# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0016_blogpost_publish_it'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='publish_it',
            field=models.BooleanField(default=False, verbose_name=b'Publish This Post'),
            preserve_default=True,
        ),
    ]
