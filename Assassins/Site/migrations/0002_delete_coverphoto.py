# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0003_remove_game_cover'),
        ('Site', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CoverPhoto',
        ),
    ]
