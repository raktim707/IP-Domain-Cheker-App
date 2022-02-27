from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('ip-address/', views.ipaddress_file, name="ip_file"),
    path('domains/', views.domain_file, name="domain_file")
]
