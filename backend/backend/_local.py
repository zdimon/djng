IS_SSL_SERVER = False
DOMAIN='http://localhost:8085'
SOCKET_SERVER='http://localhost:8888'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
import os
from .settings import BASE_DIR
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp/mail')
FRONTEND_DOMAIN='http://localhost:4200'
FRONTEND_DIR = os.path.join(os.getcwd(),'..','ng-admin')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.getenv('POSSTGRES_DB', 'dating')
POSTGRES_PASSWORD = os.getenv('POSSTGRES_PASSWORD', '1234567')
POSTGRES_USER = os.getenv('POSSTGRES_USER', 'postgres')
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
    }
}


