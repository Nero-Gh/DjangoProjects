from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets


genericView = generics.GenericAPIView
mixinsList = mixins.ListModelMixin
mixinsCreate = mixins.CreateModelMixin
mixinsUpdate = mixins.UpdateModelMixin
mixinsDestroy = mixins.DestroyModelMixin
mixinsRetrieve = mixins.RetrieveModelMixin
genericViewSet = viewsets.GenericViewSet

class EmployeeViewSet(genericViewSet,mixinsList,mixinsCreate,mixinsUpdate,mixinsDestroy):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class GenericApiView(genericView,mixinsList,mixinsCreate,mixinsRetrieve,mixinsUpdate,mixinsDestroy):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = 'id'


    def get(self,request,id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,id=None):
        return self.update(request)

    def delete(self,request,id=None):
        return self.destroy(request)

# Create your views here.
