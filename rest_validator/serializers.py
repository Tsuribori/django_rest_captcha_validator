from rest_framework import serializers
from django.core.cache import cache


class RestCaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=64)
    captcha_value = serializers.CharField(max_length=8, trim_whitespace=True)

    def validate(self, data):
        super(RestCaptchaSerializer, self).validate(data)
        key = data['captcha_key']
        value = data['captcha_value']
        real_value = cache.get(key)
        
        if value.upper() == real_value:
            cache.set(key, 'Validated')
            return data
 
        else:
            raise serializers.ValidationError('Invalid or expired CAPTCHA')
