# Generated by Django 2.2 on 2020-03-10 11:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('account', '0015_auto_20200213_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
