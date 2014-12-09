# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0013_auto_20141205_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='threat_assessment',
            field=models.CharField(default=b'Aggressive', max_length=50, null=True, verbose_name=b'Threat Assessment: In your opinion the motorist/person in question was being . . .', choices=[(b'Belligerent', b'Belligerent'), (b'Threatening', b'Threatening'), (b'Aggressive', b'Aggressive'), (b'Careless', b'Careless'), (b'Thoughtless', b'Just Plain Stupid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='what',
            field=models.TextField(verbose_name=b'Describe What Happened (be factual, include direction of travel for cyclists and vehicles, note witnesses, etc.)'),
            preserve_default=True,
        ),
    ]
