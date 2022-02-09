from modeltranslation.translator import translator, TranslationOptions
from .models import Props, Value

class PropsTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Props, PropsTranslationOptions)

class ValueTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Value, ValueTranslationOptions)