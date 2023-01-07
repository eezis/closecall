# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0020_auto_20150120_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='email_sent_on',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
