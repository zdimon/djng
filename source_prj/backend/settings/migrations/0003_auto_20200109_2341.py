# Generated by Django 2.2.4 on 2020-01-09 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_replanishmentplan_bonus_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replanishmentplan',
            name='bonus_subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.BonusSubscription'),
        ),
    ]