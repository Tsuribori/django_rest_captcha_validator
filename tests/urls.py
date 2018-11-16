from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .views import ItemView

router = routers.DefaultRouter()
router.register(r'items', ItemView, base_name='item')

urlpatterns = [
    path('validate/', include('rest_validator.urls')),
    path('captcha/', include('captcha.urls')),
    path('', include(router.urls)),
    
]
