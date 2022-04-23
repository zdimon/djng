from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from backend.local import DOMAIN
from converter import FFMpeg
from django.conf import settings

ffmpeg = FFMpeg(ffprobe_path=settings.FFPROBE_PATH, ffmpeg_path='/')


class VideoModelMixin(models.Model):
    video = models.FileField(blank=True, upload_to='user_video')
    # seconds
    duration = models.CharField(null=True, blank=True, max_length=30)

    @property
    def get_video_url(self):
        try:
            return DOMAIN + self.video.url
        except:
            return None

    class Meta:
        abstract = True

    def get_video_orientation(self):
        probe = ffmpeg.probe(self.video.path)
        if probe.video.video_width > probe.video.video_height:
            return 'land'
        else:
            return 'port'

    def get_video_duration(self):
        return str(ffmpeg.probe(self.video.path).video.duration)
