# Generated by Django 2.2.4 on 2019-12-17 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191217_1229'),
        ('blocklist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blocklist',
            name='block_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blocked_profiles', to='account.UserProfile'),
        ),
    ]
