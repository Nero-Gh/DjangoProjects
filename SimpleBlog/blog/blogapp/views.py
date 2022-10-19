from django.shortcuts import render
from .models import BlogApp

# Create your views here.

def index(request):
    blogs = BlogApp.objects.all()
    return render(request,'index.html',{'blogs':blogs})

def post(request,pk):
    blog = BlogApp.objects.get(id=pk)
    return render(request,'post.html',{'blog':blog})