from django.contrib import admin
from django.urls import path
from Company import views, views_ajax

# Name company
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




#  Ordernes, Menu, Reportes y mas
      path('order-report', views.OrderReport.as_view(), name='order-report'),
            path('orders', views.Orders.as_view(), name='orders'),
                  path('all-orders', views.AllOrders.as_view(), name='all-orders'),
            path('platos', views.Platos.as_view(), name='platos'),
      path('create-category', views.CreateCategory.as_view(), name='create-category'),
                  
# Finanzas 
      path('report', views.Report.as_view(), name='report'),


# Menu
      path('menu', views.Menu.as_view(), name='menu'),
            path('select-Menu/<int:pk>', views.SelectMenu.as_view(), name='select-menu'),


#  Reclamaciones o solicitudes
      path('claims', views.Claims.as_view(), name='claims'),
            path('create-claim', views.CreateClaim.as_view(), name='create-claim'),
                  path('update-claim/<int:pk>', views.UpdateClaim.as_view(), name='update-claim'),


# Contratos 
     path('contratos', views.Contratos.as_view(), name='contratos'),
            path('create-contrato', views.CreateContrato.as_view(), name='create-contrato'),
                  path('update-contrato/<int:pk>', views.UpdateContrato.as_view(), name='update-contrato'),
            path('detail-contrato/<int:pk>', views.DetailContrato.as_view(), name='detail-contrato'),

# Solicitudes ajax asincronas
      path('verify-username-ajax', views_ajax.Verify_Username_Ajax, name='verify-username-ajax'),
]

