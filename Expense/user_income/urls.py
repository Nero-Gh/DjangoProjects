from django.urls import path
from .views import (income,add_income,edit_income,delete_income)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', income , name="income"),
    path('add-income', add_income ,name='add-income'),
    path('edit-income/<int:id>', edit_income , name='edit-income'),
    path('delete-income/<int:id>', delete_income , name='delete-income'),
    # path('search-expenses',csrf_exempt(search_expense) , name='search-expenses'),
]