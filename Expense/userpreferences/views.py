from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

# Create your views here.


def index(request):
    # movie content from currencies json file to python dictionary
    data=[]

    # file_path=os.path.join(settings.BASE_DIR, 'currencies.json')

    file_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Accessing the json file
    # with open(file_path,'r') as json_file:
    #     data = json.load(json_file)
    #     for k,v in data.items():
    #         currency_data.append({'name':k,'value':v})

    with open(os.path.join(file_path,'currencies.json')) as json_file:
        data = json.load(json_file)
        arr =[]
        for k,v in data.items():
            arr.append({'name':k,'value':v})



    exits = UserPreference.objects.filter(user=request.user)
    user_preferences = None
    if exits:
        user_preferences=UserPreference.objects.get(user=request.user)

    if request.method == 'GET':


        # This function is to debug
        # import pdb
        # pdb.set_trace()

        return render(request, 'preferences/index.html',{'currencies':arr,'user_preference':user_preferences})

    else:
        currence = request.POST['currence']
        if exits:
            user_preferences.currence=currence
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currence=currence)
        messages.success(request,'Currency changed succesfully 😉.')
        return render(request, 'preferences/index.html',{'currencies':arr,'user_preference':user_preferences})

