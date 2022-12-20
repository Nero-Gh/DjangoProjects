from django.contrib import admin
from .models import Category,Expenses

# Register your models here.
#Customizing Expense admin Page
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount','description','owner','category','date',)
    search_fields = ('description','owner','category','date',)
    list_per_page = 5

admin.site.register(Expenses,ExpenseAdmin)
admin.site.register(Category)


