# Generated by Django 5.1.2 on 2024-11-17 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0042_carouselcursos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='core_values',
        ),
        migrations.AddField(
            model_name='about',
            name='core_value_1',
            field=models.CharField(default='Valor por defecto 1', max_length=255),
        ),
        migrations.AddField(
            model_name='about',
            name='core_value_2',
            field=models.CharField(default='Valor por defecto 2', max_length=255),
        ),
        migrations.AddField(
            model_name='about',
            name='core_value_3',
            field=models.CharField(default='Valor por defecto 3', max_length=255),
        ),
        migrations.AddField(
            model_name='about',
            name='core_value_4',
            field=models.CharField(default='Valor por defecto 4', max_length=255),
        ),
        migrations.AddField(
            model_name='about',
            name='core_value_5',
            field=models.CharField(default='Valor por defecto 5', max_length=255),
        ),
        migrations.AlterField(
            model_name='about',
            name='team_image',
            field=models.ImageField(blank=True, null=True, upload_to='about_images/'),
        ),
    ]
