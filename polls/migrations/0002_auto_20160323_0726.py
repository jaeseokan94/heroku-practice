# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 07:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseVocabularyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('choice_1', models.FileField(blank=True, default='', null=True, upload_to='', validators=[polls.models.validate_picture_extension])),
                ('choice_2', models.FileField(blank=True, default='', null=True, upload_to='', validators=[polls.models.validate_picture_extension])),
                ('choice_3', models.FileField(blank=True, default='', null=True, upload_to='', validators=[polls.models.validate_picture_extension])),
                ('choice_4', models.FileField(blank=True, default='', null=True, upload_to='', validators=[polls.models.validate_picture_extension])),
                ('choice_5', models.FileField(blank=True, default='', null=True, upload_to='', validators=[polls.models.validate_picture_extension])),
                ('choice_6', models.FileField(blank=True, default='', null=True, upload_to='', validators=[polls.models.validate_picture_extension])),
                ('correct_answer', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default=('1', '1'), max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(blank=True, max_length=50, null=True)),
                ('word_in_lang', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LevelLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceDialectItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_url', models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_audio_extension])),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RenameField(
            model_name='language',
            old_name='name2',
            new_name='name_in_language',
        ),
        migrations.RemoveField(
            model_name='exercisequestion',
            name='choice_answers',
        ),
        migrations.RemoveField(
            model_name='languagesubtopic',
            name='video_url',
        ),
        migrations.RemoveField(
            model_name='situationalvideo',
            name='video_wihtout_transcript',
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='instructions_in_language',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='choice_1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='choice_2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='choice_3',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='choice_4',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='choice_5',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='choice_6',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='question_type',
            field=models.CharField(choices=[('ty', 'Typing'), ('tf', 'True or False'), ('dd', 'Drag and Drop'), ('mc', 'Multiple Choice')], default=('ty', 'Typing'), max_length=200),
        ),
        migrations.AddField(
            model_name='languagesubtopic',
            name='grammar_video_file',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_movie_extension]),
        ),
        migrations.AddField(
            model_name='languagesubtopic',
            name='subtopic_name_in_language',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='choice_1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='choice_2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='choice_3',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='choice_4',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='choice_5',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='choice_6',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='correct_answers',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='question_text',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='situation_description_in_language',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='situationalvideo',
            name='video_without_transcript',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_movie_extension]),
        ),
        migrations.AlterField(
            model_name='dialect',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='languagetopic',
            name='topic_name_in_language',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.CharField(choices=[('Alphabet', 'Alphabet'), ('Numbers', 'Numbers'), ('Days', 'Days of the Week'), ('Holidays', 'Holidays'), ('Months', 'Seasons and Months'), ('Time', 'Time')], default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='resourceitem',
            name='audio_url',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_audio_extension]),
        ),
        migrations.AlterField(
            model_name='resourceitem',
            name='pronounciation_guide_or_date',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='resourceitem',
            name='word_in_language',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='resourceitempicture',
            name='audio_url',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_audio_extension]),
        ),
        migrations.AlterField(
            model_name='resourceitempicture',
            name='picture_url',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_picture_extension]),
        ),
        migrations.AlterField(
            model_name='situationalvideo',
            name='video_with_transcript',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[polls.models.validate_movie_extension]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Level'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='resourcedialectitem',
            name='dialect',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Dialect'),
        ),
        migrations.AddField(
            model_name='resourcedialectitem',
            name='resource_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.ResourceItem'),
        ),
        migrations.AddField(
            model_name='levellanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Language'),
        ),
        migrations.AddField(
            model_name='levellanguage',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Level'),
        ),
        migrations.AddField(
            model_name='glossary',
            name='language_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Language'),
        ),
        migrations.AddField(
            model_name='exercisevocabularyquestion',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Exercise'),
        ),
    ]