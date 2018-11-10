import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'Django>=2.1.3',
    'django-ranged-response>=0.2.0',
    'django-simple-captcha>=0.5.9',
    'djangorestframework>=3.9.0',
    'Pillow>=5.3.0',
    'pgk-resources>=0.0.0',
    'python-memcached>=1.59',
    'pytz>=2018.7',
    'six>=1.11.0'
]

setup(
    name = 'django_rest_captcha_validator',
    version = '0.1',
    packages= find_packages(),
    include_package_data = True,
    license = 'MIT License',
    description = 'A Django app to validate human input based on CAPTCHA',
    long_description = README,
    url = 'https://github.com/Tsuribori/django_rest_captcha_validator',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
