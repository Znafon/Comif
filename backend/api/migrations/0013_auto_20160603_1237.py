# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-03 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_transaction_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='cotisant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalclient',
            name='cotisant',
            field=models.BooleanField(default=False),
        ),
    ]