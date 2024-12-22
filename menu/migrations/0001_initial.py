# Generated by Django 5.1.3 on 2024-12-05 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Dish Name')),
                ('dish_type', models.CharField(choices=[('starter', 'Starter Dish'), ('first_main', 'First Main Plate'), ('second_main', 'Second Main Plate'), ('dessert', 'Dessert')], max_length=20, verbose_name='Dish Type')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Menu Name')),
                ('dessert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='desserts', to='menu.dish')),
                ('first_main_plate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_main_dishes', to='menu.dish')),
                ('second_main_plate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_main_dishes', to='menu.dish')),
                ('starter_dish', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='starter_dishes', to='menu.dish')),
            ],
        ),
    ]