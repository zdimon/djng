# Generated by Django 2.2.4 on 2019-12-05 14:02

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webmaster',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(help_text='Name', max_length=250, verbose_name='Name')),
                ('adress', models.TextField(help_text='Adress', max_length=250, verbose_name='Ardess of the office')),
                ('payment_method', models.CharField(choices=[('pb', 'Privatbank'), ('epay', 'Epay')], default='pb', max_length=50, verbose_name='Language')),
                ('contact_email', models.CharField(max_length=250, verbose_name='Email')),
                ('skype', models.CharField(default='', max_length=250, verbose_name='Email')),
                ('other_messanger', models.CharField(default='', help_text='Skype, telegram etc...', max_length=250, verbose_name='Other messangers')),
                ('country', models.CharField(default='', max_length=250, verbose_name='Country')),
                ('city', models.CharField(max_length=250, verbose_name='City')),
                ('phone', models.CharField(default='', max_length=250, verbose_name='Phone 1')),
                ('is_approved', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Webmaster',
                'verbose_name_plural': 'Webmasters',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]