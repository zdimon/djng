# Generated by Django 2.2.4 on 2019-12-25 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20191225_0916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofiledoc',
            old_name='is_approved',
            new_name='is_verified',
        ),
    ]
