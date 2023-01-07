# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141229_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='email',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Email Address', blank=True),
            preserve_default=True,
        ),
    ]
