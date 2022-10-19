from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog , name='blog'),
    path('employee/', views.home, name='employee'),
    path('form/', views.add, name='add-employee'),
    path('delete/<int:id>/', views.deleteForm , name='delete-employee'),
    path('edit/<int:id>/', views.edit , name='edit-employee'),
    path('details/', views.details , name='details'),
    path('details/<int:id>', views.detailsId , name='blog-id'),
]