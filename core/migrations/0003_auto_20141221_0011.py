# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141220_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='message',
            field=models.TextField(null=True, verbose_name=b'Your comment, question, or feedback'),
            preserve_default=True,
        ),
    ]
