# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0015_auto_20180508_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userticket',
            name='outtime',
            field=models.DateTimeField(),
        ),
    ]
