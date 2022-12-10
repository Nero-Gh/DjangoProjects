from django.urls import path
from .views import (RegistrationView,UserValidationView,EmailValidationView)
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path("register/",RegistrationView.as_view(), name='register'),
    path("validate-username",csrf_exempt(UserValidationView.as_view()), name='validate-username'),
    path("validate-email",csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
]
