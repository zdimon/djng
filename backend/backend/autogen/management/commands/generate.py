from django.core.management.base import BaseCommand, CommandError
from backend.settings import FRONTEND_DIR
from backend.settings import BASE_DIR
import json
import shutil
import os
from django.template import loader




OUT_PATH =  os.path.join(FRONTEND_DIR, 'src','app','views')


file_list = [
    'view/tpl.module.ts',
    'view/tpl.component.ts',
    'view/tpl.component.html',
    'view/list/tpl-list.component.html',
    'view/list/tpl-list.component.ts',
    'view/edit/tpl-edit.component.ts',
    'view/edit/tpl-edit.component.html',
    'store/index.ts',
    'store/_services/index.ts',
    'store/_services/tpl.service.ts',
    'store/_services/tpl.utils.ts',
    'store/_selectors/tpl.selectors.ts',
    'store/_reducers/tpl.reducers.ts',
    'store/_models/tpl.model.ts',
    'store/_effects/tpl.effects.ts',
    'store/_data-sources/tpl.datasource.ts',
    'store/_actions/tpl.actions.ts'
]


file_tab_list = [
    'view/tabs/list/tpl.component.ts',
    'view/tabs/list/tpl.component.html',
    'store/_models/tpl.tab.model.ts',
    'store/_data-sources/tpl.tab.datasource.ts',
    'store/_selectors/tpl.tab.selectors.ts',
    'store/_reducers/tpl.tab.reducers.ts',
    'store/_effects/tpl.tab.effects.ts',
    'store/_actions/tpl.tab.actions.ts',
    'store/_services/tpl.tab.services.ts',
    #'view/tabs/edit/tpl-edit-dialog.component.ts',
    #'view/tabs/edit/tpl-edit-dialog.component.html',
]

def custom_parse(source, conf):
    try:
        key = '%%%s%%' % 'class'
        source = source.replace(key,conf['class'])
    except:
        pass

    key = '%%%s%%' % 'upname'
    source = source.replace(key,conf['upname'])
    key = '%%%s%%' % 'camelName'
    source = source.replace(key,conf['camelName'])
    key = '%%%s%%' % 'fileprefix'
    source = source.replace(key,conf['fileprefix'])
    return source

def create_dirs(conf):
    root_path = '%s/src/app/views/%s' % (FRONTEND_DIR, conf['root'])
    # out_path = '%s/views/%s' % (root_path, conf['dirname'])
    # store_path = '%s/views/%s/store' % (FRONTEND_DIR, conf['dirname'])

    try:
        os.makedirs(root_path, exist_ok=True)
    except:
        pass

    app_path = os.path.join(root_path,conf['dirname'])
    try:
        shutil.rmtree(app_path)
    except:
        pass
    os.makedirs(app_path)
    os.makedirs(os.path.join(app_path,'view'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'view','list'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'view','tabs'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'view','edit'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_actions'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_services'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_selectors'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_data-sources'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_models'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_reducers'), exist_ok=True)
    os.makedirs(os.path.join(app_path,'store','_effects'), exist_ok=True)
    
def gen_tabs(conf):
    try:
        for tab in conf["tabs"]:
            print('Generating tab %s' % tab["title"])
            tab_path = os.path.join(FRONTEND_DIR, 'src','app',\
            'views', conf['root'],conf['dirname'],'view','tabs')
            os.makedirs(os.path.join(tab_path,'list'), exist_ok=True)
            os.makedirs(os.path.join(tab_path,'edit'), exist_ok=True)
            print(tab_path)

            for i in file_tab_list:
                filename = i.replace('tpl', tab['selector'])
                out_path = os.path.join(FRONTEND_DIR, 'src','app',\
                'views', conf['root'],conf['dirname'],filename)
                print(filename)

                template = loader.get_template(i)
                ext = i.split('.')[len(i.split('.'))-1]
                conf['class'] = tab['class']
                conf['selector'] = tab['selector']
                conf['list_fields'] = tab['fields']
                conf['url_list'] = tab['url_list']
                conf['url_delete'] = tab['url_delete']
                conf['url_update'] = tab['url_update']
                conf['url_create'] = tab['url_create']

                out = template.render(conf)
                out = custom_parse(out,conf)
                with open(out_path, 'w') as f:
                    f.write(out)

            # generate model
            template = loader.get_template(file_list[13])
            out_path = os.path.join(FRONTEND_DIR, 'src','app',\
                'views', conf['root'],conf['dirname'],file_list[13].replace('tpl', tab['selector']))
            out = template.render(conf)
            print(out_path)
    except Exception as e:
        print('error in generating tabs \n'+ repr(e))


def c_list(conf):
    print('Generating crud... %s' % conf['dirname'])
    
    for i in file_list:
        filename = i.replace('tpl', conf['fileprefix'])
        out_path = os.path.join(OUT_PATH, conf['root'], conf['dirname'],filename)
        template = loader.get_template(i)
        ext = i.split('.')[len(i.split('.'))-1]
        out = template.render(conf)
        out = custom_parse(out,conf)
        with open(out_path, 'w') as f:
            f.write(out)
        '''
        if ext == 'html':
            print('HTML!!!')
            fpath = os.path.join(BASE_DIR,'autogen','data',i)
            with open(fpath,'r') as f:
                txt = f.read()
            txt = custom_parse(txt,conf)
            with open(out_path, 'w') as f:
                f.write(txt)
        else:
        '''
            
            



class Command(BaseCommand):
    'Generate admin'
    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
    def handle(self, *args, **options):
        conf_path = '%s/autogen/conf/%s.json' % (BASE_DIR,options['name'])
        # print('Generating from %s to %s' % (conf_path, out_path))
        print('Read configuration %s' % conf_path)
        with open(conf_path,'r') as f:
            res = f.read()
            conf = json.loads(res)
        create_dirs(conf)
        c_list(conf)
#         print(conf)
        gen_tabs(conf)


