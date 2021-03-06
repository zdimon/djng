# Generated by Django 2.2.4 on 2019-12-04 15:45

from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('has_video', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=250)),
                ('text', models.TextField()),
                ('geo', models.CharField(max_length=50)),
                ('lon', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('city', models.CharField(max_length=250)),
                ('country', models.CharField(max_length=250)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserFeedSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_destination', to='account.UserProfile')),
                ('user_subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscriber', to='account.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserFeedMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', image_cropping.fields.ImageCropField(blank=True, upload_to='user_photo')),
                ('cropping_port', image_cropping.fields.ImageRatioField('image', '150x200', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping port')),
                ('cropping_land', image_cropping.fields.ImageRatioField('image', '200x112', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping land')),
                ('cropping_square', image_cropping.fields.ImageRatioField('image', '100x100', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping square')),
                ('croppos_port', models.CharField(default='', max_length=250)),
                ('croppos_land', models.CharField(default='', max_length=250)),
                ('croppos_square', models.CharField(default='', max_length=250)),
                ('video', models.FileField(blank=True, upload_to='user_video')),
                ('type_media', models.CharField(choices=[('photo', 'Photo'), ('video', 'Video')], default='photo', max_length=5, verbose_name='Type of media')),
                ('orient', models.CharField(choices=[('land', 'Landscape'), ('port', 'Portrait')], default='port', max_length=5, verbose_name='Orientation')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_main', models.BooleanField(default=False)),
                ('feed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedmedia', to='feed.UserFeed')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserFeedComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedcomment', to='feed.UserFeed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.UserProfile')),
            ],
        ),
    ]
