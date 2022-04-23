
from moderation.models import Moderation
from django.utils.safestring import mark_safe

from usermedia.models import UserMedia


def show_feed(feed):

    media = UserMedia.objects.filter(feed=feed)
    try:
        out = '<p><strong>%s</strong></p><p>%s</p>' % (feed.title, feed.text)
        for m in media:
            if m.type_media == 'photo':
                out += '<img src="%s" /><br />' % m.get_small_url_square
            else:
                out += '<video width="400" src="%s" autoplay controls></video><br />' % m.get_video_url
        return mark_safe(out)
    except Exception as e:
        return str(e)


def moderate_new_feed(feed):
    try:
        Moderation.objects.get(type_obj='feed-new',object_id=feed.pk)
    except:
        m = Moderation()
        m.type_obj = 'feed-new'
        m.name = 'New fed moderation'
        m.content_object = feed
        m.save()

def approve_feed(obj):
    feed = obj.content_object
    feed.is_approved = True
    feed.save()
    obj.delete()