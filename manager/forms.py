from django.forms import ModelForm
from .models import Income
from . models import Expense
class IncomeForm(ModelForm):
    class Meta:
        model =Income
        fields = ['amount','category','date']

class ExpenseForm(ModelForm):
    class Meta:
        model =Expense
        fields = ['amount','category','date']

