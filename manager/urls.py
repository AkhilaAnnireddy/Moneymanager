"""moneyman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    #auth
    path('',views.home,name='home'),
    path('signup/',views.signupuser,name='signupuser'),
    path('login/',views.loginuser,name='loginuser'),
    path('logout/',views.logoutuser,name='logoutuser'),
    #app's
    path('currentmoney/',views.currentmoney,name='currentmoney'),
    path('income/',views.updateincome,name='updateincome'),
    path('expense/',views.updateexpense,name='updateexpense'),
    path('transactions/',views.transactions,name='transactions'),
    path('income/<int:transaction_pk>',views.viewincome,name='viewincome'),
    path('expense/<int:transaction_pk>',views.viewexpense,name='viewexpense'),
    path('income/<int:income_pk>/delete',views.deleteincome,name='deleteincome'),
    path('expense/<int:expense_pk>/delete',views.deleteexpense,name='deleteexpense'),
]