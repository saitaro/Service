# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-17 05:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0004_auto_20181017_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='execution_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 18, 8, 32, 36, 793928)),
        ),
    ]
