from rest_framework import serializers
from django.core.cache import cache
from django.conf import settings

class RestCaptchaField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        
        if len(data) > 40:
            raise serializers.ValidationError('CAPTCHA key is too long.')
        cache_value = cache.get(data)
 
        if cache_value == 'Validated':
            if settings.REST_VALIDATOR_SINGLE_USE:
                cache.delete(data)
            return data

        else:
            raise serializers.ValidationError('Invalid or expired CAPTCHA')
