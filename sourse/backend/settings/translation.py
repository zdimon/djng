from modeltranslation.translator import translator, TranslationOptions
from .models import MailTemplates

class MailTemplatesTranslationOptions(TranslationOptions):
    fields = ('title','content')

translator.register(MailTemplates, MailTemplatesTranslationOptions)
