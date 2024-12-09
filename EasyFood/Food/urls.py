from django.contrib import admin
from django.urls import path
from Food import views

app_name = 'food'
urlpatterns = [

      path('dashboard', views.Dashboard.as_view(), name='dashboard'),
      
]

