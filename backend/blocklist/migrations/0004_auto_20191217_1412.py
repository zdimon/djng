# Generated by Django 2.2.4 on 2019-12-17 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blocklist', '0003_auto_20191217_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blocklist',
            name='block_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='block_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]