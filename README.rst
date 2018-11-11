=============================
Django REST CAPTCHA Validator
=============================

.. image:: https://travis-ci.com/Tsuribori/django_rest_captcha_validator.svg?branch=master
    :target: https://travis-ci.com/Tsuribori/django_rest_captcha_validator

Django REST CAPTCHA Validator is a Django package that's essentially just CAPTCHA suitable for Django REST framework.

Requirements
++++++++++++

A correctly setup cache is required, as the CAPTCHA keys are stored in the cache instead of the database. Django REST CAPTCHA Validator installs all other depedencies on it's own.

Intallation
+++++++++++

Install via pip: ::

  $ pip install -e git+https://github.com/Tsuribori/django_rest_captcha_validator#egg=rest_validator

Add rest_validator and `Django Simple Captcha <https://github.com/mbi/django-simple-captcha>`_ to your INSTALLED_APPS: ::

  INSTALLED_APPS = [
      ...
      'captcha',
      'rest_validator',
      ...
  ]

Remember to migrate: ::
  
  $ python manage.py migrate

Add entries to your urls.py: ::

  urlpatterns = [
      ...
      path('captcha/', include('captcha.urls')),
      path('validate/', include('rest_validator.urls')),
      ...
  ]

Usage
+++++

Django REST CAPTCHA Validator provides a RestCaptchaField that can be added to a serializer: ::

  from rest_validator.fields import RestCaptchaField
  from rest_framework import serializers
  from .models import Item

  class ItemSerializer(serializers.ModelSerializer):
  
      captcha_key = RestCaptchaField()
      
      class Meta:
          model = Item
          fields = ('item_text', 'captcha_key') 


The field is used in validating human input.

The package also provides a RestCaptchaView that is mapped to the URL given to it, in this case /validate/.  
A GET request to the view will generate a new CAPTCHA challenge, and return a CAPTCHA key value and an URL to the challenge image, for example: ::

  {
      "captcha_key: "e0411286a3c3f5b57d859747eb8811d3bd023b3a",
      "captcha_image": "http://localhost:8000/captcha/image/e0411286a3c3f5b57d859747eb8811d3bd023b3a/"
  }


A POST request to the view will accept "captcha_key" and "captcha_value" fields. The value of "captcha_value" must be the value of the solved CAPTCHA that "captcha_key" points to. 
On a succesful POST request with valid data the following is returned: ::

  {
      "validated": true
  }

A request with an expired "captcha_key" or invalid "captcha_value" will return: ::

  {
      "non_field_errors: [
          "Invalid or expired CAPTCHA"
      ]
  }


After a CAPTCHA is succesfully validated, the "captcha_key" of the CAPTCHA in question can be used in a serializer with a RestCaptchaField to validate human input. 
The "captcha_key" is valid as long the value exists in the cache, so it's reusable. 
If a "captcha_key" that is expired or not validated is used in a serializer, the following error occurs during serializer validation: ::

  {
      "captcha_key": [
          "Invalid or expired CAPTCHA"
      ]
  }


Settings
++++++++

There is currently only a single setting associated with Django REST CAPTCHA Validator, REST_VALIDATOR_CACHE_TIMEOUT. 
The setting, in seconds, controls how long a validated CAPTCHA persists in the cache. The default is 300 seconds. 

All other CAPTCHA settings are controlled by settings associated with Django Simple Captcha. List of those can be viewed in their `documentation <https://django-simple-captcha.readthedocs.io/en/latest/advanced.html#configuration-toggles>`_.
