from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import loader
from django.urls import reverse
from .models import Workers,BlogPost

# Create your views here.

def home(request):
    workers = Workers.objects.all()
    output =''
    
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    return render(request,'employee/index.html', {'workers':workers})


def add(request):
    name = request.POST.get('name')
    title = request.POST.get('title')

    if name and title:
        addForm = Workers(name=name, title=title)
        addForm.save()
        return HttpResponseRedirect('/employee/')

    return render(request,'employee/form.html')


def deleteForm(request,id):
    try:
        workerForm = Workers.objects.get(pk=id)
        workerForm.delete()
    except:
        raise Http404("Page Not Found 😊")
    return HttpResponseRedirect('/employee/')


def edit(request,id):
    workerForm = Workers.objects.get(pk=id)
    # template = loader.get_template('edit.html')
    context = {
        'worker':workerForm
    }

    name = request.POST.get('name')
    title = request.POST.get('title')

    if name and title:
        workerForm.name = name
        workerForm.title = title
        workerForm.save()
        return HttpResponseRedirect('/employee/')  

    return render(request,'employee/edit.html',context)






def blog(request):
    myBlog = BlogPost.objects.all()
    featuredBlog = BlogPost.objects.filter(featured=True)
    context = {
        'blogs':myBlog,
        'featuredBlogs':featuredBlog
    }
    return render(request,'employee/blog.html',context)



def details(request):
    # context = {
    #     'details':details
    # }
    return render(request,'employee/details.html')
    


def detailsId(request,id):
    details =BlogPost.objects.get(pk=id)
    context = {
        'details':details
    }
    return render(request,'employee/details.html',context)


