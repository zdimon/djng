from celery.decorators import task
import subprocess
import os
from .settings import BASE_DIR

@task
def build_front():
    out =  subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)
    path = BASE_DIR+'/../../frontend'
    os.chdir(path)
    out =  subprocess.Popen("ng build --prod", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)

@task
def build_admin():
    out =  subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)
    path = BASE_DIR+'/../../admin'
    os.chdir(path)
    out =  subprocess.Popen("ng build --prod", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)


@task
def build_dev():
    out =  subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)
    out =  subprocess.Popen("./bin/dj_migrate", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)
    path = BASE_DIR+'/../../frontend'
    os.chdir(path)
    out =  subprocess.Popen("ng build -c dev", shell=True, stdout=subprocess.PIPE).stdout.read()
    print(out)
