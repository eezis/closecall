# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0023_auto_20150126_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='threat_assessment',
            field=models.CharField(default=b'Aggressive', max_length=50, null=True, verbose_name=b'Threat Assessment: In your opinion the motorist/person in question was being . . .', choices=[(b'Belligerent', b'Belligerent - the driver was malicious and undertook deliberate actions that purposefully put lives at risk'), (b'Threatening', b'Threatening - the driver create a dangerous situation and delivered a measured threat (close, but not too close)'), (b'Aggressive', b'Aggressive - the driver was trying to scare, harass or intimidate (yelled, honked, etc)'), (b'Careless', b'Careless - the driver caused a problem but it wasnt deliberately hostile and may have been accidental'), (b'Thoughtless', b'Just Plain Stupid')]),
            preserve_default=True,
        ),
    ]
