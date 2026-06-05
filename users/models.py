from django.db import models

class User(models.Model):
    username=models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username

class Shaxs(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name