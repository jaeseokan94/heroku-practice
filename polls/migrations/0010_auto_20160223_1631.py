# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20160223_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceitem',
            name='word_in_language',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
