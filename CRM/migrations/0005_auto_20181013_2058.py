# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-13 17:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0004_auto_20181011_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='execution_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 14, 20, 58, 49, 105585)),
        ),
    ]
