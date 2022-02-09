import sys
import os
import re
from backend.settings import BASE_DIR
from django.core.management import BaseCommand
from backend.settings import FRONTEND_DIR

class Command(BaseCommand):

    @staticmethod
    def find_html(catalog):
        find_files = []
        for root, _, file in os.walk(catalog):
            find_files += [os.path.join(root, name) for name in file if ".html" == name[-5:]]
        return find_files

    @staticmethod
    def find_in_file(path):
        chats_name = []
        with open(path, encoding="latin-1") as file:
            text = file.read()
            temp = re.findall("{{.*\|\s*translate\s*}}", text)
            for i in temp:
                try:
                    chats_name.append(re.findall(r"""['"].*['"]""", i)[0].replace("'", "").replace('"', ""))
                except:
                    pass
            return chats_name

    #def add_arguments(self, parser):
    #    parser.add_argument('catalog')

    def handle(self, *args, **options):
        print("Collecting translations")
        catalog = FRONTEND_DIR
        chats = []
        print('Searching in %s' % catalog)
        html_files = Command.find_html(catalog)
        print(html_files)
        for i in html_files:
            chats += Command.find_in_file(i)
        result_str = ""
        for i in chats:
            result_str += '' if f"\"{i}\"" in result_str else f"    \"{i}\": _(\"{i}\"),\n"
        path = os.path.join(BASE_DIR, "trans", "parts", "autotrans.py")
        with open(path, "w") as file:
            file.write(
                """from django.utils.translation import ugettext_lazy as _


MAP = {
%s
}
""" % result_str
            )











