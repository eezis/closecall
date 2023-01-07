# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0015_blogpost_post_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='publish_it',
            field=models.BooleanField(default=False, verbose_name=b'Publish It'),
            preserve_default=True,
        ),
    ]
