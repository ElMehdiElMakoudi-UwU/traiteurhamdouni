# Generated by Django 4.2.7 on 2024-12-24 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_number_of_tables_event_price_of_decoration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.CharField(blank=True, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20, verbose_name='Event Status'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, choices=[('wedding', 'Wedding'), ('corporate', 'Corporate Event'), ('birthday', 'Birthday'), ('private', 'Private Party')], max_length=50, verbose_name='Event Type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='number_of_guests',
            field=models.PositiveIntegerField(blank=True, verbose_name='Number of Guests'),
        ),
        migrations.AlterField(
            model_name='event',
            name='number_of_tables',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Number of Tables'),
        ),
        migrations.AlterField(
            model_name='event',
            name='price_of_decoration',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Price of Decoration'),
        ),
        migrations.AlterField(
            model_name='event',
            name='price_of_extras',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Price of Extras'),
        ),
        migrations.AlterField(
            model_name='event',
            name='price_per_table',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Price per Table'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_address',
            field=models.TextField(blank=True, verbose_name='Venue Address'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Venue Name'),
        ),
    ]
