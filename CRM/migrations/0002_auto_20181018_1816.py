# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-18 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='execution_date',
            field=models.DateTimeField(),
        ),
    ]
