# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0009_auto_20141130_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='license_uncertain',
            field=models.CharField(max_length=150, null=True, verbose_name=b'License plate (use this input field if you are pretty sure, but not 100 percent certain)', blank=True),
            preserve_default=True,
        ),
    ]
