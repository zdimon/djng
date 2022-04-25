from modeltranslation.translator import TranslationOptions, translator
from .models import StaticPage


class StaticPageTranslationOptions(TranslationOptions):

    fields = ('title', 'content',)


translator.register(StaticPage, StaticPageTranslationOptions)


