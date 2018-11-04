from rest_framework import response, generics
from rest_framework.reverse import reverse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache
from .serializers import RestCaptchaSerializer

class RestCaptchaView(generics.GenericAPIView):

    serializer_class = RestCaptchaSerializer

    def get(self, request):
        key = CaptchaStore.generate_key()
        image = reverse('captcha-image', kwargs={'key': key}, request=request)
        value = CaptchaStore.objects.get(hashkey=key)
        cache.set(key, value.challenge)

        data = {
           'captcha_key': key,
           'captcha_image': image
        }
 
        return response.Response(data)

    def post(self, request):
        serializer_data = RestCaptchaSerializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        
        data = {
             'validated': True
        }

        return response.Response(data)
        

