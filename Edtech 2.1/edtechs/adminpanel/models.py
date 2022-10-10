from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Assignments(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    date_created=models.DateTimeField(auto_now_add=True)
    def  __str__(self):
          return self.name



class SubmitAssignments(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignments,on_delete=models.CASCADE)
    
    description=models.CharField(max_length=500,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    
    