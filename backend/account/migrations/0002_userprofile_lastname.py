# Generated by Django 2.2.4 on 2019-12-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(default='', max_length=250),
        ),
    ]
