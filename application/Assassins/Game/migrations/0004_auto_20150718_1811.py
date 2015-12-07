# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0003_remove_game_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assigned',
            field=models.DateTimeField(auto_now_add=True, auto_created=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='closed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
