# Generated by Django 4.2 on 2024-01-27 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_alter_tickettype_for_concert'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='name',
        ),
        migrations.AddField(
            model_name='ticket',
            name='Email',
            field=models.CharField(default='example@example.com', help_text="Customer's Email", max_length=100),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ForConcert',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.concert'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='TransactionID',
            field=models.CharField(default='price_xxxxxxx', help_text='Autogenerated transaction ID from STRIPE', max_length=100),
        ),
        migrations.AddField(
            model_name='ticket',
            name='Name',
            field=models.CharField(default='Customer Name', help_text="Customer's Name", max_length=60),
        ),
    ]
