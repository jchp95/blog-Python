# Generated by Django 5.1.3 on 2024-11-28 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0052_calificacion'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Calificacion',
        ),
        migrations.DeleteModel(
            name='Suscriptores',
        ),
        migrations.DeleteModel(
            name='Visitas',
        ),
    ]
