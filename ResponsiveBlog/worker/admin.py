from atexit import register
from django.contrib import admin

from .models import Workers,BlogPost



class EmployeeAdmin(admin.ModelAdmin):
    list_display= ('name','title')

class BlogTable(admin.ModelAdmin):
    list_display=('title','description','featured')


admin.site.register(Workers,EmployeeAdmin)
admin.site.register(BlogPost,BlogTable)
