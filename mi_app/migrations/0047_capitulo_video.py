# Generated by Django 5.1.3 on 2024-11-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0046_delete_cursos'),
    ]

    operations = [
        migrations.AddField(
            model_name='capitulo',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='cursos/videos/'),
        ),
    ]
