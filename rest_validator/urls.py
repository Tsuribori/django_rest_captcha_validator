from django.urls import path
from .views import RestCaptchaView

urlpatterns = [
    path('', RestCaptchaView.as_view(), name='rest_validator_view'), 
]
