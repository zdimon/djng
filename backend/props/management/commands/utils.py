from props.models import Props, Value
from django.utils.translation import ugettext_lazy as _
def load_props():
    p = Props()
    p.alias = 'eye_color'
    p.for_woman = True
    p.for_man = True
    p.name = _('Eyes color')
    p.save()

    v = Value()
    v.prop = p
    v.name = _('Blue')
    v.save()

    v = Value()
    v.prop = p
    v.name = _('Brown')
    v.save()

    p = Props()
    p.for_woman = True
    p.for_man = True
    p.alias = 'heir_color'
    p.name = _('Heir color')
    p.save()

    v = Value()
    v.prop = p
    v.name = _('Dark')
    v.save()

    v = Value()
    v.prop = p
    v.name = _('Blonde')
    v.save()

    p = Props()
    p.for_woman = True
    p.for_man = True
    p.type = 'many'
    p.alias = 'language'
    p.name = _('Language')
    p.save()

    v = Value()
    v.prop = p
    v.name = _('English')
    v.save()

    v = Value()
    v.prop = p
    v.name = _('Russian')
    v.save()