# Generated by Django 2.2.4 on 2020-01-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatcontact',
            name='is_camera',
            field=models.BooleanField(default=False),
        ),
    ]