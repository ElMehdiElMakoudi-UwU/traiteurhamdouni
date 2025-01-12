# Generated by Django 4.2.7 on 2025-01-12 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Client Name')),
                ('date', models.DateField(verbose_name='Reservation Date')),
                ('decorations_required', models.BooleanField(default=False, verbose_name='Decorations Required')),
                ('traiteur_required', models.BooleanField(default=False, verbose_name='Traiteur Required')),
                ('traiteur_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Caterer Name')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Amount')),
                ('advance_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Advance Amount')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
        ),
    ]
