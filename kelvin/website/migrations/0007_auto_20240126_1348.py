# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2024-01-26 13:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20240126_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket_type',
            old_name='name',
            new_name='ticket_label',
        ),
    ]
