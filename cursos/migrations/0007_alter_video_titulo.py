# Generated by Django 5.1.3 on 2024-11-25 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0006_video_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='titulo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
