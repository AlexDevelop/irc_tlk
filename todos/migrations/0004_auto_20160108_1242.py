# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_todolist_identifier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todolist',
            old_name='type',
            new_name='todo_type',
        ),
    ]
