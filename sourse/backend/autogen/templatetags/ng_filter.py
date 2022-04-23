from django import template
from django.utils import safestring

register = template.Library()


@register.filter(name='ng')
def Angularify(value):
  return safestring.mark_safe('{{%s}}' % value)

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg2) + str(arg1)