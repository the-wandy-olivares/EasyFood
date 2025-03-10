from django.contrib import admin
from django.urls import path
from Food import views

app_name = 'food'
urlpatterns = [

      path('', views.Restaurant.as_view(), name='restaurant'),
            path('dashboard', views.Dashboard.as_view(), name='dashboard'),
                  path('administration', views.Administration.as_view(), name='administration'),
                        path('configuration', views.Configuration.as_view(), name='configuration'),
                  path('configuracion', views.Configuracion.as_view(), name='configuracion'),
            path('despacho', views.Despacho.as_view(), name='despacho'),
]

