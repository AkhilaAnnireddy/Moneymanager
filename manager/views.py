from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from . models import Income
from . models import Expense
from .forms import IncomeForm
from .forms import ExpenseForm
from itertools import chain 
import operator
# Create your views here.
def home(request):
    return render(request,'manager/home.html')
def signupuser(request):
    if request.method=='GET':
        return render(request,'manager/signup.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentmoney')


            except IntegrityError:
                return render(request,'manager/signup.html',{'form':UserCreationForm(),'error':'username has already been taken'})

        else:
           return render(request,'manager/signup.html',{'form':UserCreationForm(),'error':'Passwords didnot match'})
        
def loginuser(request):
    if request.method =='GET':
        return render(request,'manager/login.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'manager/login.html',{'form':AuthenticationForm(), 'error':'username and password are incorrect'})
        else:
            login(request,user)
            return redirect('currentmoney')

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')   
@login_required
def currentmoney(request):
    total_income=0
    total_expense=0
    incomes= Income.objects.filter(user=request.user)
    expenses=Expense.objects.filter(user=request.user)
    for income in incomes:
        total_income+= income.amount
    for expense in expenses:
        total_expense+=expense.amount
    balance= total_income-total_expense
    return render(request,'manager/currentmoney.html',{'income':total_income,'expense':total_expense,'balance':balance})


@login_required
def updateincome(request):
    if request.method =='GET':
        return render(request,'manager/updateincome.html',{'form':IncomeForm()})
    else:
        try:
            form=IncomeForm(request.POST)
            newincome = form.save(commit=False)
            newincome.user = request.user
            newincome.save()
            return redirect('currentmoney')
        except ValueError:
            return render(request,'manager/updateincome.html',{'form':IncomeForm(),'error':'bad data passed'})

    
@login_required
def updateexpense(request):
    if request.method =='GET':
        return render(request,'manager/updateexpense.html',{'form':ExpenseForm()})
    else:
        try:
            form=ExpenseForm(request.POST)
            newexpense = form.save(commit=False)
            newexpense.user = request.user
            newexpense.save()
            return redirect('currentmoney')
        except ValueError:
            return render(request,'manager/updateexpense.html',{'form':ExpenseForm(),'error':'bad data passed'})
@login_required
def transactions(request):
    incomes=Income.objects.filter(user=request.user).order_by('-date')
    expenses=Expense.objects.filter(user=request.user).order_by('-date')
    transactions=chain(incomes, expenses)
    transactions= sorted(transactions,key=operator.attrgetter('date'), reverse= True)
    return render(request,'manager/transactions.html',{'transactions':transactions,'incomes':incomes,'expenses':expenses})

@login_required
def viewincome(request, transaction_pk):
    income=get_object_or_404(Income, pk=transaction_pk, user=request.user)
    if request.method=='GET':
        form = IncomeForm(instance=income)
        return render(request,'manager/viewincome.html',{'income':income, 'form': form})
    else:
        try:
            form=IncomeForm(request.POST,instance=income)
            form.save()
            return redirect('transactions')
        except ValueError:
            return render(request,'manager/viewincome.html',{'income':income, 'form': form, 'error':'bad info'})


@login_required            
def deleteincome(request,income_pk):
    income=get_object_or_404(Income, pk=income_pk, user=request.user)
    if request.method=='POST':
        income.delete()
        return redirect('transactions')

@login_required    
def viewexpense(request, transaction_pk):
    expense=get_object_or_404(Expense, pk=transaction_pk, user=request.user)
    if request.method=='GET':
        form = ExpenseForm(instance=expense)
        return render(request,'manager/viewexpense.html',{'expense':expense, 'form': form})
    else:
        try:
            form=ExpenseForm(request.POST,instance=expense)
            form.save()
            return redirect('transactions')
        except ValueError:
            return render(request,'manager/viewexpense.html',{'expense':expense, 'form': form, 'error':'bad info'})


@login_required
def deleteexpense(request, expense_pk):
    expense=get_object_or_404(Expense, pk=expense_pk, user=request.user)
    if request.method=='POST':
        expense.delete()
        return redirect('transactions')
    

