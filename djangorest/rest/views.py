from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer

# Create your views here.

@api_view(['GET','POST'])
def EmployeeList(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serialize_emp = EmployeeSerializer(employees, many=True)
        return Response(serialize_emp.data)

    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response( serializer.errors ,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def EmployeeId(request,id):
    employee = Employee.objects.get(id=id)
    if request.method == 'GET':
        serialize_emp = EmployeeSerializer(employee)
        return Response(serialize_emp.data)
    
    if request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




