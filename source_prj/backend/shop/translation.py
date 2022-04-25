from modeltranslation.translator import TranslationOptions, translator
from shop.models import CategoryProduct, Product


class ProductTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


translator.register(Product, ProductTranslationOptions)


class CategoryProductTranslationOptions(TranslationOptions):

    fields = ('title',)


translator.register(CategoryProduct, CategoryProductTranslationOptions)