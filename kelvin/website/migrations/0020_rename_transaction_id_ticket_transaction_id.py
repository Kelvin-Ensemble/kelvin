# Generated by Django 4.2 on 2024-01-27 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_rename_email_ticket_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='transaction_id',
            new_name='transaction_ID',
        ),
    ]
