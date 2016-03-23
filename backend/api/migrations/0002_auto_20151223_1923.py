# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='prenom',
        ),
        migrations.AlterField(
            model_name='client',
            name='nom',
            field=models.CharField(max_length=300),
        ),
    ]
