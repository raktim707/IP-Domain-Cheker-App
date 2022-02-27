from django.contrib import admin
from .models import IpAddress, Domain_Name

# Register your models here.

admin.site.register(IpAddress)
admin.site.register(Domain_Name)