from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expenses
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
from userpreferences.models import UserPreference
from datetime import datetime,timedelta
import csv
import  xlwt
import pdfkit
# Create your views here.
# The @login prevents the user to go back to the home page after 
# being logged out
@login_required(login_url='authentication/login')
def expenses(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)

    paginator = Paginator(expenses,10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    # currency = UserPreference.objects.filter(user = request.user).currence
    currency = ''
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
    }

    return render(request,'expenses/index.html',context)

@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    mydate = request.POST
    context =  {
        'categories':categories,
        'value':mydate,
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
    

@login_required(login_url='authentication/login')
def edit_expense(request,id):
    expenses= Expenses.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'expenses':expenses,
        'values':expenses,
        'categories':categories
    }
    if request.method =='GET':
        return render(request,'expenses/edit_expense.html',context)


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


@login_required(login_url='authentication/login')
def delete_expense(request,id):
    expenses = Expenses.objects.get(pk=id)
    expenses.delete()
    messages.warning(request,'Expense deleted successfully.')
    return redirect('expenses')


@login_required(login_url='authentication/login')
def search_expense(request):
    if request.method=='POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expenses.objects.filter(amount__istartswith=search_str,owner=request.user) | Expenses.objects.filter(date__istartswith=search_str,owner=request.user) | Expenses.objects.filter(description__istartswith=search_str,owner=request.user) | Expenses.objects.filter(category__istartswith=search_str,owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)



def expense_category_summary(request):
    today = datetime.now()
    six_months_go = today+timedelta(days=180)
    expenses = Expenses.objects.filter(owner=request.user ,date__gte = six_months_go, date__lte = today)

    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category,expenses)))

    def get_expense_category_amount(category):
        amount = 0;
        filter_by_category = expenses.filter(category=category)

        for item in filter_by_category:
            amount += item.amount

        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)

    return  JsonResponse({'expense_category_data':finalrep}, safe=False)


def state_view(request):
    return render(request,'expenses/stats.html')



def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    expenses = Expenses.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.now())+'.xls'


    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Expenses')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns=['Amount','Description','Category','Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style.font.bold=False

    rows = Expenses.objects.filter(owner=request.user).values_list('amount','description','category','date')


    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)

    return response



def export_pdf(request):

# Query the data from the model
    people = Expenses.objects.filter(owner=request.user)

    # Create the HTML content for the PDF
    # html = '<h1>Expenses</h1>'
    # html += '<table>'
    # html += '<tr><th>Amount</th><th>Description</th><th>Category</th><th>date</th></tr>'
    # for person in people:
    #     html += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(person.amount, person.description, person.category, person.date)
    # html += '</table>'
    context = {
        'expenses':people,
    }
    html = render(request,'expenses/expense_pdf.html',context)

    # Generate the PDF from the HTML
    pdf = pdfkit.from_string(html, False)

    # Create the HTTP response with the PDF as an attachment
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses.pdf'

    return response
