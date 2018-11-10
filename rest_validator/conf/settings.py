from django.conf import settings

REST_VALIDATOR_CACHE_TIMEOUT = getattr(settings, 'REST_CAPTCHA_VALIDATOR_TIMEOUT', 300)


