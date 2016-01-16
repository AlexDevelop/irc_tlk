# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0004_auto_20160108_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='status',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
