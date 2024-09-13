# Generated by Django 4.2 on 2024-01-28 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_tickettype_display_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='Concert_Nickname',
            field=models.CharField(default='Concert', help_text='This is just a nickname for this concert to make it easier for you to distinguish in the admin page.', max_length=40),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='Linked_Tickets',
            field=models.ManyToManyField(blank=True, help_text='Use this to select which tickets should have their ticket quantities synced. (Make sure they are selected on all linked tickets)', to='website.tickettype'),
        ),
    ]