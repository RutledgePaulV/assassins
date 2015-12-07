# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoverPhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='covers')),
                ('thumb', models.ImageField(null=True, blank=True, upload_to='covers/thumbs')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=128, choices=[('ALABAMA', 'Alabama'), ('ALASKA', 'Alaska'), ('ARIZONA', 'Arizona'), ('ARKANSAS', 'Arkansas'), ('CALIFORNIA', 'California'), ('COLORADO', 'Colorado'), ('CONNECTICUT', 'Connecticut'), ('DELAWARE', 'Delaware'), ('FLORIDA', 'Florida'), ('GEORGIA', 'Georgia'), ('HAWAII', 'Hawaii'), ('IDAHO', 'Idaho'), ('ILLINOIS', 'Illinois'), ('INDIANA', 'Indiana'), ('IOWA', 'Iowa'), ('KANSAS', 'Kansas'), ('KENTUCKY', 'Kentucky'), ('LOUISIANA', 'Louisiana'), ('MAINE', 'Maine'), ('MARYLAND', 'Maryland'), ('MASSACHUSETTS', 'Massachusetts'), ('MICHIGAN', 'Michigan'), ('MINNESOTA', 'Minnesota'), ('MISSISSIPPI', 'Mississippi'), ('MISSOURI', 'Missouri'), ('MONTANA', 'Montana'), ('NEBRASKA', 'Nebraska'), ('NEVADA', 'Nevada'), ('NEW HAMPSHIRE', 'New Hampshire'), ('NEW JERSEY', 'New Jersey'), ('NEW MEXICO', 'New Mexico'), ('NEW YORK', 'New York'), ('NORTH CAROLINA', 'North Carolina'), ('NORTH DAKOTA', 'North Dakota'), ('OHIO', 'Ohio'), ('OKLAHOMA', 'Oklahoma'), ('OREGON', 'Oregon'), ('PENNSYLVANIA', 'Pennsylvania'), ('RHODE ISLAND', 'Rhode Island'), ('SOUTH CAROLINA', 'South Carolina'), ('SOUTH DAKOTA', 'South Dakota'), ('TENNESSEE', 'Tennessee'), ('TEXAS', 'Texas'), ('UTAH', 'Utah'), ('VERMONT', 'Vermont'), ('VIRGINIA', 'Virginia'), ('WASHINGTON', 'Washington'), ('WEST VIRGINIA', 'West Virginia'), ('WISCONSIN', 'Wisconsin'), ('WYOMING', 'Wyoming')])),
                ('city', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='SocialMediaPhotos',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.URLField()),
                ('thumb', models.URLField(null=True, blank=True)),
            ],
        ),
    ]
