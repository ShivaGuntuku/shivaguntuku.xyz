# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20170912_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='read_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
