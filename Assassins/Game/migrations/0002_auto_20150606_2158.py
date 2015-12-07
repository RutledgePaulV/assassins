# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='players'),
        ),
        migrations.AddField(
            model_name='game',
            name='reviewers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='reviewers'),
        ),
        migrations.AddField(
            model_name='game',
            name='rules',
            field=models.ForeignKey(to='Game.RuleSet', related_name='rules'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='game',
            field=models.ForeignKey(to='Game.Game'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='killee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='killee'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='killer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='killer'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announcement',
            name='game',
            field=models.ForeignKey(to='Game.Game'),
        ),
    ]
