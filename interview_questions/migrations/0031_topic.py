# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-03 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview_questions', '0030_auto_20160711_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('screenname', models.CharField(max_length=30)),
            ],
        ),
    ]
