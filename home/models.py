from django.db import models

# Create your models here.
class Signin(models.Model):
    username= models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    password=models.CharField(max_length=122)

    def __str__(self):
        return self.username
    
class Test(models.Model):
    location= models.CharField(max_length=122)
    checkin=models.DateField(null=True,blank=True)
    checkout=models.DateField(null=True,blank=True)
    guest=models.IntegerField()
    