# Generated by Django 2.2.4 on 2020-02-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatmessage_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='type',
            field=models.CharField(choices=[('message', 'message'), ('video', 'video'), ('image', 'image'), ('sticker', 'sticker'), ('post', 'post')], default='message', max_length=10, verbose_name='Type of message'),
        ),
    ]