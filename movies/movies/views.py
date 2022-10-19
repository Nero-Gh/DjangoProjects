from turtle import title
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render

from .models import Movies

def movies(request):
    data= Movies.objects.all()
    return render(request,'movies/movie.html',{'movies':data})

def home(request):
    return HttpResponse("Welcome to Homepage")

def detail(request,id):
    data = Movies.objects.get(pk=id)
    return render(request,'movies/detail.html',{'movie':data})

def add(request):
    title = request.POST.get('title')
    year = request.POST.get('year')

    if title and year:
        movie = Movies(title=title, year=year)
        movie.save()
        return HttpResponseRedirect('/movies')
    return render(request, 'movies/add.html')


def delete(request,id):
    try:
        movie =Movies.objects.get(pk=id)
    except:
        raise Http404("Page not found")
    movie.delete()
    return HttpResponseRedirect('/movies')