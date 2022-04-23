# Generated by Django 2.2.4 on 2019-12-25 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20191225_1158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofiledoc',
            old_name='is_verified',
            new_name='is_approved',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]