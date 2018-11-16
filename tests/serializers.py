from rest_validator.fields import RestCaptchaField
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    
    captcha_key = RestCaptchaField()
    
    class Meta:
        model = Item
        fields = ('item_text', 'captcha_key')

    def create(self, validated_data):
        validated_data.pop('captcha_key')
        instance = super().create(validated_data)
        return instance
