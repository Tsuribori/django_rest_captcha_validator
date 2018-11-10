from rest_framework import serializers
from django.core.cache import cache

class RestCaptchaField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        
        if len(data) > 40:
            raise serializers.ValidationError('CAPTCHA key is too long.')
        cache_value = cache.get(data)
 
        if cache_value == 'Validated':
            return data

        else:
            raise serializers.ValidationError('Invalid or expired CAPTCHA')
