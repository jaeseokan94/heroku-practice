# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_auto_20160322_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossary',
            name='word',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='word_in_lang',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='situationalvideo',
            name='correct_answers',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='situationalvideo',
            name='question_text',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]