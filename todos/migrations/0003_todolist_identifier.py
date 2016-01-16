# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_auto_20160108_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='identifier',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
