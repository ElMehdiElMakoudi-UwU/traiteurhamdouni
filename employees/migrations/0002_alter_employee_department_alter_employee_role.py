# Generated by Django 4.2.7 on 2024-12-25 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.CharField(choices=[('decoration', 'Décoration'), ('cooking', 'Cuisine'), ('service', 'Service'), ('logistics', 'Logistique'), ('managment', 'Gestion')], max_length=50, verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('manager', 'Manager'), ('staff', 'Staff'), ('chef', 'Chef'), ('photograph', 'Photograph')], max_length=50, verbose_name='Role'),
        ),
    ]
