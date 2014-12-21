# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0013_auto_20141221_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='about_the_author',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='author',
        ),
    ]
