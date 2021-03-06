# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-11 09:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interview_questions', '0022_auto_20160710_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('obj', models.TextField(max_length=20)),
                ('obj_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelManagers(
            name='problem',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='vote',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='interview_questions.Votes'),
        ),
    ]
