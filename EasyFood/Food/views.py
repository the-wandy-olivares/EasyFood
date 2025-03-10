from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View, CreateView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from datetime import datetime
from django.utils import timezone

from Company import models

from .models  import ConfigurationApp
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.cache import cache_page


class Dashboard(TemplateView):
      template_name = "food/dashboard.html"

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            
            if not hasattr(request.user, 'restaurant') or not request.user.restaurant:
                  if request.user.employee_profile.role == "estandar":
                        return redirect('company:no-acces-to-view')  
            return super().get(request, *args, **kwargs)    
            

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] = ''
            return context
    


    # Restaurante, Menu, Plato, Ingrediente, Categoria y Producto

class Restaurant(TemplateView):
      template_name = "food/restaurant/restaurant.html"

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            if  hasattr(request.user, 'restaurant'):
               return redirect(reverse('company:admin-company'))
            return super().get(request, *args, **kwargs)

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.employee_profile.role == "representante":
                  context['categorias'] = models.MenuChoices.objects.filter(company=self.request.user.employee_profile.company, role="ejecutivo", is_active=True)
            else:
                  context['categorias'] = models.MenuChoices.objects.filter(company=self.request.user.employee_profile.company, role=self.request.user.employee_profile.role, is_active=True)
            categoria_id = self.request.GET.get('id')
            if categoria_id:
                  context['platos'] = models.Category.objects.get(id=categoria_id)
            return context

      def post(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return HttpResponseForbidden()

            order_data = json.loads(request.POST.get('orders', '[]'))
            for item in order_data:
                  name = item.get('name')
                  price = item.get('price')
                  img = item.get('img')
                  category = item.get('category')
                  plato = models.Plato.objects.get(id=item.get('plato'))
                  orden = models.Order(name=name, price=price, img=img , category=models.Category.objects.get(id=category),
                              plato=plato,
                              employee=request.user.employee_profile,
                              company=request.user.employee_profile.company,
                              )
                  orden.save()
                  print(orden.name)

            messages.success(request, "Order created successfully!")
            return redirect(reverse('company:orders'))


# Administracion, Proveedores, Clientes, Comisiones y Ventas
class Administration(TemplateView):
      template_name = "food/administration/administration.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context



# Configuracion, Cambiar contraseña, Cambiar correo electronico y Mas
class Configuration(TemplateView):
      template_name = "food/configuration/configuration.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['configuration'] = ConfigurationApp.objects.get(id=2)
            return context

      def post(self, request, *args, **kwargs):
            configuration = ConfigurationApp.objects.get(id=1)
            print( request.POST.get('animations'))
            if request.POST.get('animations'):
                  if configuration.animations == True:
                        configuration.animations = False
                  else:
                        configuration.animations = True
                  configuration.save()
            return redirect(reverse('food:configuration'))


class Despacho(TemplateView):
      template_name = "food/despacho/despacho.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            category_id = self.request.GET.get('category')
            company_id = self.request.GET.get('company')
            status = self.request.GET.get('status')

            orders = models.Order.objects.all()
            if status ==  None:
                  status = 'preparando'
                  orders = orders.filter(status=status)


            if status:
                  orders = orders.filter(status=status)
            if category_id:
                  orders = orders.filter(category_id=category_id)
            if company_id:
                  orders = orders.filter(company_id=company_id)
                  
            orders_by_company = {}
            for order in orders:
                  company_name = order.company.name
                  company_img = order.company.img.url if order.company.img else None
                  if company_name not in orders_by_company:
                              orders_by_company[company_name] = {
                                    'orders': [],
                                    'img': company_img
                              }
                  orders_by_company[company_name]['orders'].append(order)

            context['orders_by_company'] = orders_by_company  # Pass the grouped orders to the context
            # context['companies'] = models.Company.objects.filter(is_active=True)
            context['companies'] = models.Company.objects.filter(
                        is_active=True,
                        orders_company__status__in=[ 'preparando', 'enviado']
            ).distinct()
            context['categories'] = models.Category.objects.all()
            return context
      
    

      def post(self, request):
      # Obtener los platos seleccionados desde el formulario (IDs de platos seleccionados)
            if request.POST.getlist('ids[]'):
                  orders = models.Order.objects.filter(id__in=request.POST.getlist('ids[]'))
                  for order in orders:
                        order.status = 'enviado'
                        order.save()
            return redirect(reverse('food:despacho'))



# Configuracion, Cambiar contraseña, Cambiar correo electronico y Mas
class Configuracion(TemplateView):
      template_name = "restaurante/configuracion.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
