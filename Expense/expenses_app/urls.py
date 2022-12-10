from django.urls import path
from .views import (expenses,add_expense)


urlpatterns = [
    path('',expenses, name="expenses"),
    path('add-expense',add_expense,name='add-expense')
]
