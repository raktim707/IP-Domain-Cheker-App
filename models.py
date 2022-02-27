from django.db import models

# Create your models here.
class IpAddress(models.Model):
    ip_address = models.TextField()
    ipv4=models.BooleanField()
    
    def __str__(self):
        return ip_address

class Domain_Name(models.Model):
    domain = models.TextField()
    def __str__(self):
        return domain

