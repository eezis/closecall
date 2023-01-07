# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20141221_1706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userblogprofile',
            old_name='author',
            new_name='byline',
        ),
    ]
