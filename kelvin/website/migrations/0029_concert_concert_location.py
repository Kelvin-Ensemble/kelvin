# Generated by Django 4.2 on 2024-01-27 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_remove_tickettype_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='Concert_location',
            field=models.TextField(default=''),
        ),
    ]
