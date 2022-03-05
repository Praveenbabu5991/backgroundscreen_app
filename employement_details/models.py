from django.db import models

# Create your models here.
class Employmentdetails(models.Model):
    company=models.CharField(max_length=200)
    
