from django.conf import settings
from django.utils import timezone
from django.core.exceptions import AppRegistryNotReady

REST_VALIDATOR_CACHE_TIMEOUT = getattr(settings, 'REST_CAPTCHA_VALIDATOR_TIMEOUT', 300)
CAPTCHA_TIMEOUT = getattr(settings, 'CAPTCHA_TIMEOUT', 5) #5 is the default CAPTCHA_TIMEOUT of Django Simple Captcha
