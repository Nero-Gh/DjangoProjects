from django.urls import path
from .views import (expenses,add_expense,edit_expense,delete_expense,search_expense ,expense_category_summary,state_view,export_csv,export_excel,export_pdf)
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('', expenses , name="expenses"),
    path('add-expense', add_expense ,name='add-expense'),
    path('edit-expense/<int:id>', edit_expense , name='edit-expense'),
    path('delete-expense/<int:id>', delete_expense , name='delete-expense'),
    path('search-expenses',csrf_exempt(search_expense) , name='search-expenses'),
    path('expense-category-summary',expense_category_summary, name='expense-category-summary'),
    path('stats',state_view, name='stats'),
    path('export-csv',export_csv, name='export-csv'),
    path('export-excel',export_excel, name='export-excel'),
    path('export-pdf',export_pdf, name='export-pdf'),
]
