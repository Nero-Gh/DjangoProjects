from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expenses
from django.contrib import messages

# Create your views here.
# The @login prevents the user to go back to the home page after 
# being logged out
@login_required(login_url='authentication/login')
def expenses(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    context = {
        'expenses':expenses,
    }

    return render(request,'expenses/index.html',context)

def add_expense(request):
    categories = Category.objects.all()
    context =  {
        'categories':categories,
        'values':request.POST
    }
    if request.method=='GET':
        return render(request,'expenses/add_expense.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category=request.POST['category']
        expense_date = request.POST['expense_date']
        
        if not amount:
            messages.error(request,'Amount is required.')
            return render(request,'expenses/add_expense.html',context)
 
    if request.method == 'POST':
        if not description:
            messages.error(request,'Description is required.')
            return render(request,'expenses/add_expense.html',context)
    

    Expenses.objects.create(owner=request.user, amount=amount,date=expense_date,category=category,description=description)

    messages.success(request,'Expenses added successfully')

    return redirect('expenses')
    


def edit_expense(request,id):
    expenses= Expenses.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'expenses':expenses,
        'values':expenses,
        'categories':categories
    }
    if request.method =='GET':
        return render(request,'expenses/edit-expense.html',context)


    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category=request.POST['category']
        expense_date = request.POST['expense_date']
        
        if not amount:
            messages.error(request,'Amount is required.')
            return render(request,'expenses/edit_expense.html',context)
 
        if request.method == 'POST':
            if not description:
                messages.error(request,'Description is required.')
                return render(request,'expenses/edit_expense.html',context)
    

            expenses.owner=request.user
            expenses.amount = amount
            expenses.date = expense_date
            expenses.category=category
            expenses.description=description
            
            expenses.save()


            messages.success(request,'Expense Updated successfully')

            return redirect('expenses')



def delete_expense(request,id):
    expenses = Expenses.objects.get(pk=id)
    expenses.delete()
    messages.warning(request,'Expense deleted successfully.')
    return redirect('expenses')



