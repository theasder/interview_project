# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 10:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview_questions', '0007_auto_20160620_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='position',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='problem',
            name='wiki_answer',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
