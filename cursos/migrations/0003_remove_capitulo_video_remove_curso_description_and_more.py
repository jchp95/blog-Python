# Generated by Django 5.1.3 on 2024-11-24 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_capitulo_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capitulo',
            name='video',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='description',
        ),
        migrations.AddField(
            model_name='capitulo',
            name='contenido',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
