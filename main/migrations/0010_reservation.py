# Generated by Django 5.2 on 2025-07-11 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_utilisateur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_chambre', models.CharField(choices=[('studio', 'Studio'), ('chambre_3p', 'Chambre 3 personnes'), ('chambre_4p', 'Chambre 4 personnes'), ('chambre_5p', 'Chambre 5 personnes')], max_length=20)),
                ('date_arrivee', models.DateField()),
                ('date_depart', models.DateField()),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
                ('hebergement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='main.hebergement')),
                ('utilisateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='main.utilisateur')),
            ],
        ),
    ]
