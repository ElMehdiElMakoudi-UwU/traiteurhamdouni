# Generated by Django 4.2.7 on 2024-12-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_event_menu_remove_event_special_instructions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='number_of_guests',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Number of Guests'),
        ),
    ]