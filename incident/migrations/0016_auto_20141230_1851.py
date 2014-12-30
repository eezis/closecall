# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0015_incident_witnesses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='witnesses',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Full Name and Phone or Email of Witnesses ( this field is not published )', blank=True),
            preserve_default=True,
        ),
    ]
