from django.contrib import admin
from django.urls import path
from Company import views


app_name = 'company'
urlpatterns = [
      
      path('admin-company', views.AdminCompany.as_view(), name='admin-company'),
      path('create-company', views.CreateCompany.as_view(), name='create-company'),

]
