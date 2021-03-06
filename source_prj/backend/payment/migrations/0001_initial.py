# Generated by Django 2.2.4 on 2019-12-09 09:33

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agency', '__first__'),
        ('account', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(help_text='Alias', max_length=250, verbose_name='Alias')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='User')),
                ('name', models.CharField(help_text='Name', max_length=250, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('ammount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='User')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_closed', models.BooleanField(default=True)),
                ('agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency', to='agency.Agency')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer', to='account.UserProfile')),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciver', to='account.UserProfile')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.PaymentType')),
            ],
            options={
                'verbose_name': 'User payment',
                'verbose_name_plural': 'User payments',
            },
        ),
    ]
