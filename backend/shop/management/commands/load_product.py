import json
import random
from django.core.files import File

from django.core.management import BaseCommand

from backend.settings import BASE_DIR
from shop.models import CategoryProduct, Product


def insert_one(d):
    print('Saving....%s' % d['title_en'])
    p = Product()
    p.id = d['id']
    p.title_en = d['title_en']
    p.title_ru = d['title_ru']
    p.price = d['price']
    p.description_ru = d['description_ru']
    p.description_en = d['description_en']
    p.category = CategoryProduct.objects.get(id=d["category"])

    filepath = BASE_DIR + '/test_data/shop/product_files/%s.jpg' % random.randint(1, 10)
    with open(filepath, 'rb') as image:
        p.picture.save('%s_%s.jpeg' % (p.id, d["category"]), File(image), save=True)

    p.save()


class Command(BaseCommand):

    help = "Import product into DB"

    def handle(self, *args, **options):
        print("Importing product...")
        Product.objects.all().delete()
        path = BASE_DIR + "/test_data/shop/product.json"
        with open(path) as f:
            data = f.read()
            jdata = json.loads(data)
            for i in jdata:
                insert_one(i)
