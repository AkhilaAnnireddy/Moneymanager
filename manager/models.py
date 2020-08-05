from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Income(models.Model):
    amount=models.IntegerField(default=0)
    category=models.CharField(max_length=25)
    date=models.DateTimeField(null=True, blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category
class Expense(models.Model):
    amount= models.IntegerField(default=0)
    category=models.CharField(max_length=25)
    date=models.DateTimeField(null=True, blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category


