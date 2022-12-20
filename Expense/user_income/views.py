from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import UserIncome,Source
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
# from userpreferences.models import UserPreference
from userpreferences.models import UserPreference

# Create your views here.
@login_required(login_url='authentication/login')
def income(request):
    # source = Source.objects.all()
    user_income = UserIncome.objects.filter(owner=request.user)

    paginator = Paginator(user_income,10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    # currency = UserPreference.objects.filter(user = request.user).currence
    context = {
        'income':user_income,
        'page_obj':page_obj,
        'currency':'',
    }

    return render(request,'income/index.html',context)

@login_required(login_url='authentication/login')
def add_income(request):
    sources = Source.objects.all()
    mydate = request.POST
    context =  {
        'sources':sources,
        'value':mydate,
    }
    if request.method=='GET':
        return render(request,'income/add_income.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source=request.POST['source']
        income_date = request.POST['income_date']
        
        if not amount:
            messages.error(request,'Amount is required.')
            return render(request,'income/add_income.html',context)
 
    if request.method == 'POST':
        if not description:
            messages.error(request,'Description is required.')
            return render(request,'income/add_income.html',context)
    

    UserIncome.objects.create(owner=request.user, amount=amount,date=income_date,source=source,description=description)

    messages.success(request,'Income added successfully')

    return redirect('income')


@login_required(login_url='authentication/login')
def edit_income(request,id):
    user_income= UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    context={
        'income':user_income,
        'values':user_income,
        'source':source
    }
    if request.method =='GET':
        return render(request,'income/edit_income.html',context)


    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source=request.POST['source']
        income_date = request.POST['income_date']
        
        if not amount:
            messages.error(request,'Amount is required.')
            return render(request,'income/edit_income.html',context)
 
        if request.method == 'POST':
            if not description:
                messages.error(request,'Description is required.')
                return render(request,'income/edit_income.html',context)
    

            user_income.owner=request.user
            user_income.amount = amount
            user_income.date = income_date
            user_income.source=source
            user_income.description=description
            
            user_income.save()


            messages.success(request,'Income Updated successfully')

            return redirect('income')


@login_required(login_url='authentication/login')
def delete_income(request,id):
    user_income = UserIncome.objects.get(pk=id)
    user_income.delete()
    messages.warning(request,'Income deleted successfully.')
    return redirect('income')



@login_required(login_url='authentication/login')
def search_income(request):
    if request.method=='POST':
        search_str = json.loads(request.body).get('searchText')

        user_income = UserIncome.objects.filter(amount__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(date__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(description__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(category__istartswith=search_str,owner=request.user)

        data = user_income.values()

        return JsonResponse(list(data), safe=False)
