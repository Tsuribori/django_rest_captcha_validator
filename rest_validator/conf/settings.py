from django.conf import settings

REST_VALIDATOR_CACHE_TIMEOUT = getattr(settings, 'REST_CAPTCHA_VALIDATOR_TIMEOUT', 300)
REST_VALIDATOR_SINGLE_USE = getattr(settings, 'REST_VALIDATOR_SINGE_USE', True)
CAPTCHA_TIMEOUT = getattr(settings, 'CAPTCHA_TIMEOUT', 5) #5 is the default CAPTCHA_TIMEOUT of Django Simple Captcha

