from django.urls import path
from .views import EmployeeList,EmployeeId

urlpatterns = [
    path('Employees/', EmployeeList),
    path('Employees/<int:id>/', EmployeeId)
]
