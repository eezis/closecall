# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0021_auto_20150126_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='threat_assessment',
            field=models.CharField(default=b'Aggressive', max_length=50, null=True, verbose_name=b'Threat Assessment: In your opinion the motorist/person in question was being . . .', choices=[(b'Belligerent', b'Belligerent - the driver undertook deliberate actions and purposefully put lives at risk'), (b'Threatening', b'Threatening - the driver engaged in active harrassment and created a dangerous situation'), (b'Aggressive', b'Aggressive - the driver may have been trying to scare or intimidate'), (b'Careless', b'Careless - the driver caused a problem but it didnt seem to be intentional'), (b'Thoughtless', b'Just Plain Stupid')]),
            preserve_default=True,
        ),
    ]
