# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0018_blogpost_social_buttons'),
    ]

    operations = [
        migrations.AddField(
            model_name='inthenews',
            name='show_it',
            field=models.BooleanField(default=False, verbose_name=b'Publish/Make Visible at site'),
            preserve_default=True,
        ),
    ]
