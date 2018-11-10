from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('validate/', include('rest_validator.urls')),
    path('captcha/', include('captcha.urls')),
]
