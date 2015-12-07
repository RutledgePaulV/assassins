# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('should_email', models.BooleanField(default=True)),
                ('should_text', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=10, null=True, blank=True)),
                ('slogan', models.CharField(max_length=255, null=True, blank=True)),
                ('biography', models.TextField(max_length=1024, null=True, blank=True)),
                ('image', models.ImageField(null=True, blank=True, upload_to='profile_pictures')),
                ('thumb', models.ImageField(null=True, blank=True, upload_to='profile_pictures/thumbs')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set', related_query_name='user')),
                ('profile', models.OneToOneField(to='Member.Profile')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set', related_query_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
