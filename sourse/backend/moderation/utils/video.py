
from moderation.models import Moderation
from django.utils.safestring import mark_safe


def moderate_new_video(video):
    m = Moderation()
    m.type_obj = 'video-new'
    m.name = 'New video moderation'
    m.content_object = video
    m.save()


def moderate_delete(video):
    m = Moderation()
    m.type_obj = 'video-delete'
    m.name = 'Delete video moderation'
    m.content_object = photo
    m.save()


def show_video(video):
    try:
        return mark_safe('<video width="400" src="%s" autoplay controls></video>' % video.video_url)
    except:
        return 'none'

def approve_video(obj):
    photo = obj.content_object
    photo.is_approved = True
    photo.save()
    obj.delete()

def disapprove_photo(obj):
    photo = obj.content_object
    photo.delete()
    obj.delete()

def delete_video(obj):
    video = obj.content_object
    video.delete()


def notdelete_video(obj):
    photo = obj.content_object
    photo.is_deleted = False
    photo.save()
    obj.delete()
