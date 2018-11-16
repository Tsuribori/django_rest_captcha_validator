from captcha.models import CaptchaStore
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from time import sleep

from .models import Item
from .serializers import ItemSerializer
from rest_validator.serializers import RestCaptchaSerializer
from rest_validator.fields import RestCaptchaField

class ViewTestCase(APITestCase):

    def setUp(self):
        self.get_resp = self.client.get(reverse('rest_validator_view'))
        self.key = self.get_resp.data['captcha_key']
        value = CaptchaStore.objects.get(hashkey=self.key)
        post_data = {'captcha_key': self.key, 'captcha_value': value}
        self.post_resp = self.client.post(reverse('rest_validator_view'), post_data)
        wrong_post_data = {'captcha_key': self.key, 'captcha_value': 'Wrong'}
        self.wrong_post_resp = self.client.post(reverse('rest_validator_view'), wrong_post_data)

    def test_view_get_status(self):
        self.assertEqual(self.get_resp.status_code, 200)
 
    def test_captcha_key(self):
        self.assertTrue(self.key)

    def test_image_link(self):
        request = self.get_resp.wsgi_request
        image_link = reverse('captcha-image', kwargs={'key': self.key}, request=request)
        self.assertEqual(self.get_resp.data['captcha_image'], image_link)

 
    def test_view_post_status(self):
        self.assertEqual(self.post_resp.status_code, 200)

    def test_validated(self):
        self.assertEqual(self.post_resp.data['validated'], True)

 
    def test_view_wrong_post_status(self):
        self.assertEqual(self.wrong_post_resp.status_code, 400)
    
    def test_wrong_post_content(self):
        self.assertEqual(self.wrong_post_resp.data['non_field_errors'], ['Invalid or expired CAPTCHA'])


class FieldTestCase(APITestCase):

    def setUp(self):
        resp = self.client.get(reverse('rest_validator_view'))
        self.key = resp.data['captcha_key']
        value = CaptchaStore.objects.get(hashkey=self.key)
        post_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': self.key, 'captcha_value': value})
        self.item = Item.objects.create(item_text='Test')
       
    def tearDown(self):
        settings.REST_VALIDATOR_SINGLE_USE = True
 
    def test_valid_field(self):
        data = {'item_text': self.item.item_text, 'captcha_key': self.key}
        serializer = ItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_too_long(self):
        long_string = ''.join('1' for i in range(0, 41))
        data = {'item_text': self.item.item_text, 'captcha_key': long_string} 
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {'captcha_key': ['CAPTCHA key is too long.']})
        

    def test_invalid_captcha_key(self):
        data = {'item_text': self.item.item_text, 'captcha_key': 'Non-valid'}
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {'captcha_key': ['Invalid or expired CAPTCHA']})
 
    def test_cache_deleted(self):
        data = {'item_text': self.item.item_text, 'captcha_key': self.key}
        serializer = ItemSerializer(data=data)
        serializer.is_valid() 
        self.assertIsNone(cache.get(self.key))

    def test_cache_not_deleted(self):
        settings.REST_VALIDATOR_SINGLE_USE = False
        data = {'item_text': self.item.item_text, 'captcha_key': self.key}
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(cache.get(self.key), 'Validated')


class SerializerTestCase(APITestCase):
    
    def setUp(self):
        get_resp = self.client.get(reverse('rest_validator_view'))
        self.key = get_resp.data['captcha_key']
        self.value = CaptchaStore.objects.get(hashkey=self.key).challenge

    def test_captcha_value_in_cache(self):
        self.assertEqual(cache.get(self.key), self.value)

    def test_validated_value_in_cache(self):
        post_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': self.key, 'captcha_value': self.value})
        self.assertEqual(cache.get(self.key), 'Validated')

    def test_no_change_on_incorrect_value(self):
        post_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': self.key, 'captcha_value': 'Wrong'})
        self.assertEqual(cache.get(self.key), self.value)

    def test_expired_captcha(self):
        old_CAPTCHA_TIMEOUT = settings.CAPTCHA_TIMEOUT
        settings.CAPTCHA_TIMEOUT = 0.0001
        key = CaptchaStore.generate_key()
        value = CaptchaStore.objects.get(hashkey=key).challenge
        post_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': key, 'captcha_value': value})
        settings.CAPTCHA_TIMEOUT = old_CAPTCHA_TIMEOUT
        sleep(0.15)
        self.assertEqual(post_resp.data['non_field_errors'], ['Invalid or expired CAPTCHA'])

    def test_expired_validation(self):
        old_VALIDATOR_TIMEOUT = settings.REST_VALIDATOR_CACHE_TIMEOUT
        settings.REST_VALIDATOR_CACHE_TIMEOUT = 0.1
        post_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': self.key, 'captcha_value': self.value})
        settings.REST_VALIDATOR_CACHE_TIMEOUT = old_VALIDATOR_TIMEOUT
        sleep(0.15)
        item = Item.objects.create(item_text='test')
        serializer = ItemSerializer(data={'item_text': item.item_text, 'captcha_key': self.key})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {'captcha_key': ['Invalid or expired CAPTCHA']})
       


class ItemCreationTestCase(APITestCase): #Test that the field works in practice

    def setUp(self):
        captcha_get_resp = self.client.get(reverse('rest_validator_view'))
        key = captcha_get_resp.data['captcha_key']
        value = CaptchaStore.objects.get(hashkey=key).challenge
        captcha_post_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': key, 'captcha_value': value})
        self.resp = self.client.post(reverse('item-list'), {'item_text': 'Test', 'captcha_key': key})

    def test_create_view_status(self):
        self.assertEqual(self.resp.status_code, 201)


class SettingsTestCase(APITestCase): #Test that default CAPTCHA_TIMEOUT of Django Simple Captcha is 5 minutes
    
    def setUp(self):
        now = timezone.now()
        captcha = CaptchaStore.generate_key()
        captcha_timeout = CaptchaStore.objects.get(hashkey=captcha).expiration
        timeout_object = captcha_timeout - now
        self.timeout = timeout_object.seconds / 60

    def test_captcha_timeout(self):
        self.assertEqual(settings.CAPTCHA_TIMEOUT, self.timeout)
       


