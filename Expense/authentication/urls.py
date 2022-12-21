from django.urls import path
from .views import (RegistrationView,UserValidationView,EmailValidationView,VerificationView,CompletedPasswordReset,LoginView,RequestPassowrdEmail,LogoutView)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register",RegistrationView.as_view(), name='register'),
    path("login",LoginView.as_view(), name='login'),
    path("logout",LogoutView.as_view(), name='logout'),
    path("reset-password",RequestPassowrdEmail.as_view(), name='reset-password'),
    path("set-new-password/<uidb64>/<token>",CompletedPasswordReset.as_view(), name='reset-user-password'),
    path("validate-username",csrf_exempt(UserValidationView.as_view()), name='validate-username'),
    path("validate-email",csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path("activate/<uidb64>/<token>",csrf_exempt(VerificationView.as_view()), name='activate'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
