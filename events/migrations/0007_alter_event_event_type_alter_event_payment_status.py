# Generated by Django 4.2.7 on 2024-12-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_number_of_guests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, choices=[('wedding', 'Mariage'), ('corporate', "Événement d'entreprise"), ('birthday', 'Anniversaire'), ('private', 'Fête privée'), ('engagement', 'Fiançailles'), ('baptism', 'Baptême'), ('marriage_signature', "Signature d'acte de mariage"), ('family_reunion', 'Réunion de famille'), ('conference', 'Conférence'), ('charity_event', 'Événement caritatif'), ('graduation', 'Remise de diplômes'), ('baby_shower', 'Fête de naissance'), ('festival', 'Festival'), ('exhibition', 'Exposition'), ('concert', 'Concert'), ('anniversary', 'Anniversaire de mariage'), ('new_year', 'Nouvel An'), ('retirement', 'Départ à la retraite')], max_length=50, verbose_name='Event Type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'En attente'), ('partial', 'Avance'), ('paid', 'Payé')], default='pending', max_length=20, verbose_name='Payment Status'),
        ),
    ]
