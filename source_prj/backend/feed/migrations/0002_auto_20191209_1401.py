# Generated by Django 2.2.4 on 2019-12-09 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfeedsubscription',
            unique_together={('user_subscriber', 'user_destination')},
        ),
    ]
