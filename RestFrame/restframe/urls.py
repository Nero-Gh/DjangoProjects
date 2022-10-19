from django.urls import path,include

from .views import GenericApiView
from rest_framework import routers


# router = routers.SimpleRouter()
# router.register('Employee',P)

urlpatterns = [
    path('GenericApiView/<int:id>/', GenericApiView.as_view())
]
