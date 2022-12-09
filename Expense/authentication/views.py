from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


# Create your views here.

class UserValidationView(View):
    
    def post(self,request):

        # this takes data from the FORM body
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({"username_error":"Username should only contain alpha numeric characters!"}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"Sorry username already exit, choose a new one."}, status = 409)

        return JsonResponse({"Username":True})
       


class RegistrationView(View):
    
    def get(self,request):
        return render(request,'authentication/register.html')
