# Generated by Django 4.2 on 2024-01-27 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_alter_ticket_email_alter_ticket_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='ForConcert',
            new_name='for_concert',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='TransactionID',
            new_name='transaction_id',
        ),
    ]
