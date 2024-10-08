# Generated by Django 4.2 on 2024-01-27 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_ticket_type_for_concert_alter_ticket_type_ticket_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_type',
            name='for_concert',
            field=models.OneToOneField(default=None, help_text='Please select the matching concert here. Make sure this is selected or the ticket will not show.', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='website.concert'),
        ),
    ]
