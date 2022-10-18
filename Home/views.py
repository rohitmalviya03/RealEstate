from time import timezone
from django.shortcuts import render,redirect
from Home.models import CustomerRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import pywhatkit
# Create your views here.
from datetime import datetime
from django.utils.timezone import utc


def Homepage(request):
    
    return render(request,'index.html')

def MainBoard(request):
    count={}
    Total=CustomerRecord.objects.all().count()
    Activated=CustomerRecord.objects.filter(Status='Activated').values().count()
    
    Not_Activated=CustomerRecord.objects.filter(Status='Not Active').values().count()
    
    Blocked=CustomerRecord.objects.filter(Status='Blocked').values().count()
    print("aaa",Blocked)
    count['Total']=Total
    count['Activated']=Activated
    count['Not_Activated']=Not_Activated
    count['Blocked']=Blocked
    
    return render(request,"dashboard.html",count)  

def Add_Contact(request):
    if request.method == "POST":
        print(request.method)
        name = request.POST.get('CName')
        Contact_No=request.POST.get('Contact_No')
        Location=request.POST.get('Location')
        customer = CustomerRecord(Name=name,City=Location,ContactNo=Contact_No)
        print(name,Contact_No)
        print("ss",customer)
        msg={}
        customer.save()
        msg['success']="Recored Saved Successfully"
        return redirect("CustomerTbl")    
    else:
        
        print(request.method)
        return render(request,'add_contact.html')     





def ViewPhoneBook(request):

    TblData={}
    Customers = CustomerRecord.showCustomers()
    print("viewdata",Customers)
        
    TblData['Customers'] =Customers
    return render(request,"phonebook.html",TblData)
import xlwt

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S.No', 'Name', 'Contact No', 'Status' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
def ViewCustomers(request):
    print(request.method)  
    TblData={} 
    if request.method == "POST":    
        print(request.method)
        filterValue =request.POST.get('filter')
        print("filter",filterValue)
        cust = CustomerRecord.getCustomersByStatus(filterValue)
        print("filtdata",cust)
        TblData['Customers']=cust
        
        return render(request,"CustomersTbl.html",TblData)
    elif request.method == "GET":
        
        # users = paginator.page(paginator.num_pages)
        # print("users",users)
        Customers = CustomerRecord.showCustomers()
        # # user_list = User.objects.all()
        page = request.GET.get('page', 1)
        # print(page,"get meaya")
        paginator = Paginator(Customers, 5)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        
        # TblData['Customers']=Customers
        TblData['user']=users
        return render(request,"CustomersTbl.html",TblData)


def listing(request):
    contact_list = CustomerRecord.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})


def UpdateStatus(request):
    data={}
    
    print("helo m",request.method)
    if request.method == "POST":
        name = request.POST.get('name')
        city=request.POST.get('city')
        contactno=request.POST.get('contactno')
        status=request.POST.get('status')
        CustId = request.session['CustId']
        print("sa",name,status)
        print("post mr",CustId)
        # customer = CustomerRecord.getData(CustId)
        # print(customer)
        Customers = CustomerRecord.showCustomers()
        TblData={}
        TblData['user'] =Customers
        cust=CustomerRecord.objects.get(id=CustId)
        print("cus",cust.Status)
        cust.Status=status
        cust.save()
        return render(request,'CustomersTbl.html',TblData)    
    else:
        CustId=request.GET.get('custId')
        request.session['CustId']=CustId
        print('session',request.session['CustId'])
        customer = CustomerRecord.getData(CustId)
        data['customer'] =customer
        print("id",CustId)
        print("customer",customer)
        print("else",request.method)
        return render(request,'UpdateData.html',data)  

def deleteCustomer(request):
    msg={}
    if request.method=="POST":
        CustId = request.session['CustId']
        print(CustId)
        cust=CustomerRecord.objects.get(id=CustId)
        print(cust)
        cust.delete()
        msg['Status'] ="Customer is Deleted"
        return render(request,"UpdateData.html",msg)
    else:
        return render(request,"UpdateData.html")        