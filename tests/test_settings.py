import os

DEBUG = True
LANGUAGE_CODE = 'en_us'
USE_TZ = True
SECRET_KEY = 'dsadjafe30w3459rag,sm32053+'


ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'tests',
    'captcha',
    'rest_framework',
    'rest_validator',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3'),
    }
}

CACHES = {
    'default' : {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
