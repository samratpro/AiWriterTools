# Generated by Django 4.2.2 on 2023-06-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_openaiapimodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeAPIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('API_Key', models.CharField(max_length=500)),
            ],
        ),
    ]
