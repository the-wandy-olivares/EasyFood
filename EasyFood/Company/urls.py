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
      # path('categorias', views.Categorias.as_view(), name='categorias'),
      path('create-category', views.CreateCategory.as_view(), name='create-category'),
            path('update-category/<int:pk>', views.UpdateCategory.as_view(), name='update-category'),
                        path('create-plato', views.CreatePlato.as_view(), name='create-plato'),
                              path('update-plato/<int:pk>', views.UpdatePlato.as_view(), name='update-plato'),
                        path('desactivar-plato/<int:pk>', views.DesactivarPlato.as_view(), name='desactivar-plato'),
                  path('realize-order-company/<int:pk>', views.RealizeOrderCompany.as_view(), name='realize-order-company'),
            path('enviar-order',  views.EnviarOrder.as_view(), name='enviar-order' ),

# Finanzas 
      path('report', views.Report.as_view(), name='report'),


# Menu
      path('menu', views.Menu.as_view(), name='menu'),
            path('select-Menu/<int:pk>', views.SelectMenu.as_view(), name='select-menu'),
                  path('create-category-for-company/<int:pk>', views.CreateCategoryForCompany.as_view(), name='create-category-for-company'),

#  Reclamaciones o solicitudes
      path('claims', views.Claims.as_view(), name='claims'),
            path('create-claim', views.CreateClaim.as_view(), name='create-claim'),
                  path('update-claim/<int:pk>', views.UpdateClaim.as_view(), name='update-claim'),


# Contratos 
      path('contratos', views.Contratos.as_view(), name='contratos'),
            path('create-contrato/<int:pk>', views.CreateContrato.as_view(), name='create-contrato'),
                  path('update-contrato/<int:pk>', views.UpdateContrato.as_view(), name='update-contrato'),
            path('detail-contrato/<int:pk>', views.DetailContrato.as_view(), name='detail-contrato'),
      path('contratos-company/<int:pk>', views.ContratosCompany.as_view(), name='contratos-company'),


#  Perfil de usuario
      path('my-profile', views.MyProfile.as_view(), name='my-profile'),
            path('delete-account', views.DeleteAccount.as_view(), name='delete-account'),
                  path('logout', views.Logout, name='logout'),

# Recuperar contraseña
      path('recovery-password', views.RecoveryPassword.as_view(), name='recovery-password'),
            path('verify-code', views.VerifyCode.as_view(), name='verify-code'),


# Solicitudes ajax asincronas
      path('verify-username-ajax', views_ajax.Verify_Username_Ajax, name='verify-username-ajax'),
            path('upload-masive-user', views_ajax.Upload_Masive_User, name='upload-masive-user'),
]

