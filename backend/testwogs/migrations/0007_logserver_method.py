# Generated by Django 2.2.4 on 2020-02-26 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testwogs', '0006_logserver_is_failed'),
    ]

    operations = [
        migrations.AddField(
            model_name='logserver',
            name='method',
            field=models.CharField(default='GET', max_length=200),
        ),
    ]