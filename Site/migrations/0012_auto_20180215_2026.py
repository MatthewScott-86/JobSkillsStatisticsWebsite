# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-16 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0011_jobposting_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobposting',
            name='category',
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='state',
            field=models.CharField(blank=True, default='', help_text='State abbreviations only.', max_length=2),
        ),
    ]
