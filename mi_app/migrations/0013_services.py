# Generated by Django 5.1.2 on 2024-11-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0012_auto_20241102_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
    ]
