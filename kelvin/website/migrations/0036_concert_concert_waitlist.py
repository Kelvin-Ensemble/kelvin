# Generated by Django 4.2 on 2024-02-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_alter_tickettype_total_ticket_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='Concert_waitlist',
            field=models.TextField(blank=True, default=''),
        ),
    ]