# Generated by Django 3.2.20 on 2024-10-31 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0002_noticia'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='noticias/'),
        ),
    ]
