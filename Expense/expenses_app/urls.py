from django.urls import path
from .views import (expenses,add_expense,edit_expense,delete_expense,search_expense)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', expenses , name="expenses"),
    path('add-expense', add_expense ,name='add-expense'),
    path('edit-expense/<int:id>', edit_expense , name='edit-expense'),
    path('delete-expense/<int:id>', delete_expense , name='delete-expense'),
    path('search-expenses',csrf_exempt(search_expense) , name='search-expenses'),
]
