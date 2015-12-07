# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('subject', models.CharField(max_length=255)),
                ('html', models.TextField(max_length=512)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('assigned', models.DateTimeField(auto_now_add=True)),
                ('closed', models.DateTimeField(null=True, blank=True, default=False)),
                ('killer_verdict', models.NullBooleanField()),
                ('killee_verdict', models.NullBooleanField()),
                ('admin_verdict', models.NullBooleanField()),
                ('status', models.CharField(max_length=1, choices=[('F', 'Failed'), ('S', 'Success'), ('I', 'Incomplete'), ('P', 'Pending')], default='I')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('intro', models.TextField(max_length=512)),
                ('hash', models.CharField(unique=True, max_length=255, null=True, blank=True)),
                ('in_progress', models.BooleanField(default=False)),
                ('open', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('cover', models.ForeignKey(to='Site.CoverPhoto')),
                ('location', models.ForeignKey(to='Site.Location')),
            ],
        ),
        migrations.CreateModel(
            name='RuleSet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('public', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('html', models.TextField(max_length=2048)),
                ('icon_class', models.CharField(max_length=255)),
            ],
        ),
    ]
