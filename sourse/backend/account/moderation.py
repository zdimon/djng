from moderation.models import Moderation

def moderate_new(doc):
    m = Moderation()
    m.type_obj = 'verify-doc'
    m.name = 'Profile status verification'
    m.content_object = doc
    m.save()
