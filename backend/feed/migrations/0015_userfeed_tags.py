# Generated by Django 2.2 on 2020-03-17 08:51

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('feed', '0014_userfeed_is_stories'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeed',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
