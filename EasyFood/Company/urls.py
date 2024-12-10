from django.contrib import admin
from django.urls import path
from Company import views


app_name = 'company'
urlpatterns = [
      
# Administracion de compañias
      path('admin-company', views.AdminCompany.as_view(), name='admin-company'),
            path('create-company', views.CreateCompany.as_view(), name='create-company'),
                  path('update-company/<int:pk>', views.UpdateCompany.as_view(), name='update-company'),
                        path('profile-company/<int:pk>', views.ProfileCompany.as_view(), name='profile-company'),
                  
#Administracion empleados
      path('create-employee/<int:pk>', views.CreateEmploye.as_view(), name='create-employee'),
            path('update-employe/<int:pk>', views.UpdateEmploye.as_view(), name='update-employee'),


# Seguridas de vistas, redirecciones y mas
      path('no-acces-to-view', views.NoAcceso_to_View.as_view(), name='no-acces-to-view'),
      path('logins', views.Employee_Login, name='logins'),
]
