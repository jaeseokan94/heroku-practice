# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 19:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_remove_languagetopic_topic_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='languagetopic',
            name='topic_name_in_english',
        ),
    ]
