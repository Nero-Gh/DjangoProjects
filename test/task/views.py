from django.urls import reverse
from django.shortcuts import render,redirect
from django import forms

# Create your views here.
# tasks = ['Bimark','Aladin','Nero']

class NewTaskForm(forms.Form):
    task = forms.CharField(label="Add New Task")
    prioity = forms.IntegerField(label="Priority",min_value=1,max_value=10 )


def index(request):  
    if "tasks" not in request.session:
        request.session["tasks"]=[]
    return render(request,"tasks/index.html",{"tasks":request.session["tasks"]})


def add(request):
    if request.method == "POST":    #checking if the reques form is post
        form = NewTaskForm(request.POST) #takin the imput and saving it in the forms variable
        if form.is_valid():#checking to see if the form is valid
            task = form.cleaned_data["task"] #getting the items in form and assigned it to task
            request.session["tasks"] +=[task] #add new the task to the list
            return redirect(reverse("tasks:index"))
        else:
            return render(request,'tasks/add.html',{"form":form})
    return render(request,'tasks/add.html',{"forms":NewTaskForm()})
