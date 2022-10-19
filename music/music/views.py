from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render
from .models import Music

def home(request):
    return HttpResponse('Welcome to the home page')

def music(request):
    data = Music.objects.all()
    return render(request,'music/music.html',{'data':data})

def details(request,id):
    try:
        data = Music.objects.get(pk=id)
    except:
        raise Http404("Page not found 😥")
    return render(request,'music/details.html',{'data':data})

def add(request):
    title = request.POST.get('title')
    year = request.POST.get('year')

    if title and year:
        music = Music(title=title, year=year)
        music.save()
    
        return HttpResponseRedirect('/music')

    return render(request,'music/add.html')


def delete(request,id):
    try:
        music = Music.objects.get(pk=id)
    except:
        raise Http404("Page not found Please Go back 😓")
    music.delete()


    return HttpResponseRedirect('/music')


def edit(request,id):
    data = Music.objects.get(pk=id)
    title = request.POST.get('title')
    year = request.POST.get('year')

    if title and year:
        music = Music(title=title, year=year)
        music.save()
        return HttpResponseRedirect('/music')
    return render(request, 'music/edit.html',{'data':data})