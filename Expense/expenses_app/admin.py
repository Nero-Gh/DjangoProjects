from django.contrib import admin
from .models import Category,Expenses

# Register your models here.

admin.site.register(Expenses)
admin.site.register(Category)


