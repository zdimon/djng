from django.db import models
from django.utils.translation import ugettext_lazy as _


class CategoryProduct(models.Model):
    title = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='product_category_files')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='product_files')
    description = models.TextField()
    price = models.IntegerField()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


