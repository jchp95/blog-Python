# Generated by Django 5.1.2 on 2024-11-15 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0040_remove_cursos_image_cursos_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cursos',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
