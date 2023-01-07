# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0017_auto_20141222_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='social_buttons',
            field=models.BooleanField(default=True, verbose_name=b'Show Social-Sharing Buttons'),
            preserve_default=True,
        ),
    ]
