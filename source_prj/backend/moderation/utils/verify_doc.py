
from moderation.models import Moderation
from django.utils.safestring import mark_safe


def approve_verify_doc(obj):
    doc = obj.content_object
    doc.is_approved = True
    doc.save()
    doc.user.is_verified = True
    doc.user.save()
    obj.delete()