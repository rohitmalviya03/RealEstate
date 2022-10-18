
from pyexpat import model
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models import Count
# Create your models here.
class Users(models.Model):
    Name = models.CharField(max_length=100)
    U_Type = models.CharField(max_length=120)
    password =models.CharField(max_length=150)
    
class CustomerRecord(models.Model):
    Name = models.CharField(max_length=200 ,default="ABC")
    City = models.CharField(max_length=200,default="CITY")
    ContactNo = models.IntegerField()
    Status =models.CharField(max_length=200,default="Not Active")

   
    @staticmethod
    def showCustomers():
        return CustomerRecord.objects.all() 
    @staticmethod
    def getData(id):
        return CustomerRecord.objects.filter(id=id)
    @staticmethod
    def getCustomersByStatus(status):
        return CustomerRecord.objects.filter(Status=status)

    