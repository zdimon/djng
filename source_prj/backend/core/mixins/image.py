from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from backend.local import DOMAIN

from easy_thumbnails.processors import filters
from PIL import ImageFilter
from PIL import Image, ImageFilter

class ImageModelMixin(models.Model):
    image = ImageCropField(blank=True, upload_to='user_photo')
    cropping_port = ImageRatioField('image', '150x200')
    cropping_land = ImageRatioField('image', '200x112')
    cropping_square = ImageRatioField('image', '100x100')
    croppos_port = models.CharField(default='', max_length=250, null=True, blank=True)
    croppos_land = models.CharField(default='', max_length=250, null=True, blank=True)
    croppos_square = models.CharField(default='', max_length=250, null=True, blank=True)

    class Meta:
        abstract = True

    def update_thumbs(self):
        self.get_small_url_port
        self.get_middle_url_port
        self.get_small_url_land
        self.get_middle_url_land
        self.get_small_url_square
        self.get_middle_url_square
        self.get_url_blur

    #### Portrait image

    @property
    def get_small_url_port(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (75, 100),
            'box': self.cropping_port,
            'crop': 'smart',
            # 'upscale': True,

        }).url

    @property
    def get_middle_url_port(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (150, 200),
            'box': self.cropping_port,
            'crop': 'smart',
            # 'upscale': True,
        }).url

    @property
    def get_small_img_port(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_small_url_port)
        except:
            return None

    @property
    def get_middle_img_port(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_middle_url_port)
        except:
            return None

    ##########

    #### Landscape image

    @property
    def get_small_url_land(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 56),
            'box': self.cropping_land,
            'crop': 'smart',
            # 'upscale': True,
        }).url

    @property
    def get_middle_url_land(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (200, 112),
            'box': self.cropping_land,
            'crop': 'smart',
            # 'upscale': True,
        }).url

    @property
    def get_small_img_land(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_small_url_land)
        except:
            return None

    @property
    def get_middle_img_land(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_middle_url_land)
        except:
            return None

    ##########

    #### Square image

    @property
    def get_small_url_square(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 100),
            'box': self.cropping_square,
            'crop': 'smart',
            'upscale': True,
        }).url

    @property
    def get_middle_url_square(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (200, 200),
            'box': self.cropping_square,
            'crop': 'smart',
            'upscale': True,
        }).url

    @property
    def get_small_img_square(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_small_url_square)
        except:
            return None

    @property
    def get_middle_img_square(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_middle_url_square)
        except:
            return None

    ##########

    @property
    def image_big(self):
        try:
            return '%s%s' % (DOMAIN, self.image.url)
        except:
            return None

    @property
    def small_main_image_url(self):
        if self.orient == 'port':
            return self.get_small_url_port
        else:
            return self.get_small_url_land

    @property
    def middle_main_image_url(self):
        if self.orient == 'port':
            return self.get_middle_url_port
        else:
            return self.get_middle_url_land

    @property
    def get_url_blur(self):
        return DOMAIN + get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 100),
            'box': self.cropping_square,
            'crop': 'smart',
            'upscale': True,
            'quality': 1,
            'replace_alpha': '#FF1493'
        }).url

    @property
    def get_img_blur(self):
        try:
            return mark_safe('<img src="%s" />' % self.get_url_blur)
        except:
            return None