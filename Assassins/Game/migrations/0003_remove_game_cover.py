# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_auto_20150606_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='cover',
        ),
    ]
