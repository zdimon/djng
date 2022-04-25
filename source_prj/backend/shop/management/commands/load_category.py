import json
import random

from django.core.management import BaseCommand
from django.core.files import File
from backend.settings import BASE_DIR
from shop.models import CategoryProduct


def insert_one(d):
    print('Saving....%s' % d['title_en'])
    c = CategoryProduct()
    c.id = d['id']
    c.title_en = d['title_en']
    c.title_ru = d['title_ru']
    filepath = BASE_DIR + '/test_data/shop/product_category_files/%s.jpg' % random.randint(1, 10)
    with open(filepath, 'rb') as image:
        c.picture.save('%s.jpeg' % c.id, File(image), save=True)
    c.save()


class Command(BaseCommand):

    help = "Import category into DB"

    def handle(self, *args, **options):
        print("Importing category...")
        CategoryProduct.objects.all().delete()
        path = BASE_DIR + "/test_data/shop/category.json"
        with open(path) as f:
            data = f.read()
            jdata = json.loads(data)
            for i in jdata:
                insert_one(i)
