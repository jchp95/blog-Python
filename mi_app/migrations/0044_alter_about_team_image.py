# Generated by Django 5.1.2 on 2024-11-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0043_remove_about_core_values_about_core_value_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='team_image',
            field=models.ImageField(blank=True, null=True, upload_to='team_images/'),
        ),
    ]
