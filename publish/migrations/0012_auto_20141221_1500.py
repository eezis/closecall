# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publish', '0011_auto_20141221_0359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-created'], 'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='reviewed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='user',
            field=models.ForeignKey(default=32, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
