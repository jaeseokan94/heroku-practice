# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_auto_20160217_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situationalvideo',
            name='video_wihtout_transcript',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]