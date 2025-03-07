from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import json
from django.views.generic import TemplateView, View, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.db.models import Sum
from collections import defaultdict
from datetime import datetime,  timedelta
from django.utils import timezone
from django.core.mail import send_mail
import random
import calendar
# http://127.0.0.1:8000/company/logins

# From my apps
from Company import models
from Company import forms



def Check_Role(view_func):
      def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                  if not hasattr(request.user, 'restaurant') or not request.user.restaurant:
                        if request.user.employee_profile.role == "ejecutivo" or "representante":
                              return view_func(request, *args, **kwargs)
            return redirect('company:no-acces-to-view')  # Reemplaza 'some_view_name' con el nombre de la vista a redirigir
      return _wrapped_view


class NoAcceso_to_View(TemplateView):
            template_name = "company/limitation-acces/no-acces-to-view.html"

            def get(self, request, *args, **kwargs):
                  if not request.user.is_authenticated:
                        return redirect(reverse('company:logins'))

                  if request.user.username != 'admin' or 'untalwandy':
                              if request.user.employee_profile.role == "ejecutivo":
                                    return redirect('food:dashboard') 
                  return super().get(request, *args, **kwargs)    

                  
                  

class AdminCompany(TemplateView):
      template_name = "company/admin-company.html"

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)    
            

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.filter(is_active=True, restaurant=self.request.user.restaurant)
            return context
    

class CreateCompany(CreateView):
      model = models.Company
      form_class = forms.Company
      template_name = "company/create-company.html" 
       # Tu plantilla personalizada
      # success_url = reverse_lazy('company:admin')  # Redirige después de guardar

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.filter(is_active=True)
            return context
            
      def form_valid(self, form):            
            form.instance.restaurant = self.request.user.restaurant
            form.save()
            employe = models.Employee.objects.get(id=self.kwargs.get('pk'))
            employe.company = form.instance
            employe.save()
            # Agrega lógica adicional aquí si es necesario
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)
            return super().form_invalid(form)

      def get_success_url(self):
            # Usamos self.object para acceder al objeto actualizado
            return reverse_lazy('company:create-contrato', kwargs={'pk': self.object.id})


@method_decorator(Check_Role, name='dispatch')
class UpdateCompany(UpdateView):
      model = models.Company
      form_class = forms.Company
      template_name = "company/update-company.html"  # Tu plantilla personalizada

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.get(is_active=True,  id=self.kwargs.get('pk'))
            return context
            
      def form_valid(self, form):
            return super().form_valid(form)

      def get_success_url(self):
            # Usamos self.object para acceder al objeto actualizado
            return reverse_lazy('company:update-company', kwargs={'pk': self.object.id})


      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)    

# @method_decorator(Check_Role, name='dispatch')

# @method_decorator(login_required, name='dispatch')  # Asegurarse de que el usuario esté autenticado
class ProfileCompany(DetailView):
      model = models.Company
      form_class = forms.Company
      template_name = "company/profile-company.html"
      success_url = reverse_lazy('company:admin-company')  # Redirige después de guardar
      context_object_name = "company"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            company = self.object  # Obtener la empresa actual

            # Obtener empleados activos en la empresa
            context['contrato'] = models.Contract.objects.get(company=company, is_active=True) if models.Contract.objects.filter(company=company, is_active=True).exists() else None
            context['employee'] = models.Employee.objects.filter(company=company)
            context['count'] = models.Employee.objects.filter(company=company, is_active=True).count()

            total_facturado = company.invoices.filter(is_facturado=True).aggregate(Sum('amount'))['amount__sum'] or 0
            
            context['total_facturado'] = total_facturado
            context['menus_choices'] = models.MenuChoices.objects.filter(company=company)

            company = models.Company.objects.get(id=self.kwargs['pk'])
            orders = models.Order.objects.filter(company= company, status='entregado')
            orders_p = models.Order.objects.filter(company= company, status='pendiente')
            orders_e = models.Order.objects.filter(company= company, status='enviado')
            orders_p_p = models.Order.objects.filter(company=company, status__in=['pendiente', 'preparando', 'enviado'])

            context['total'] = sum(order.price for order in orders)
            context['total_pendiente'] = sum(order.price for order in orders_p_p)
            context['total_entregado'] = sum(order.price for order in orders_e)
            context['invoice'] = models.Invoice.objects.filter(company=company)
            return context

      def form_valid(self, form):
            company = form.save()
            return super().form_valid(form)

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)
      

      def post(self, request, *args, **kwargs):
            menus_selected = request.POST.getlist('menus')  # Menús seleccionados
            all_menus = models.MenuChoices.objects.filter(company_id=self.kwargs['pk'])  # Todos los menús relacionados
            
            for menu in all_menus:
                  if str(menu.id) in menus_selected:  # Si el menú está seleccionado
                        role = request.POST.get(f'role_{menu.id}')
                        menu.is_active = True
                        menu.role = role
                  else:  # Si el menú no está seleccionado
                        menu.is_active = False
                  menu.save()
            
            if request.POST.get('pay'):
                  company = models.Company.objects.get(id=self.kwargs['pk'])
                  company.total_to_pay -=  int(request.POST.get('pay'))
                  company.total_pay +=  int(request.POST.get('pay'))
                  company.save()
                  models.Movements(
                        mount = company.total_to_pay,
                        description= company.name + 'Pago de ordenes',
                  ).save()
                  models.Invoice(
                        company= company,
                        amount= int(request.POST.get('pay')),
                  ).save()
            
            return redirect(reverse('company:profile-company', kwargs={'pk': self.kwargs['pk']}))

# Empleados
@method_decorator(Check_Role, name='dispatch')
class CreateEmploye(CreateView):
      model = models.Employee
      form_class = forms.Employee
      template_name = "company/employee/create-employee.html"  # Tu plantilla personalizada

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.get(is_active=True,  id=self.kwargs.get('pk'))
            return context
            
      def form_valid(self, form):

            user  = User(
                  username= form.instance.email,
                  email= form.instance.email,
                  first_name= form.instance.first_name,
                  last_name= form.instance.last_name,
            )
            # Establecer la clave del usuario
            password = form.instance.password # Reemplázalo por la clave que necesites
            user.set_password(password)
            user.save()
            
            form.instance.user = user
            form.instance.company = models.Company.objects.get(is_active=True,  id=self.kwargs.get('pk'))
            form.save()
            return super().form_valid(form)

      def get_success_url(self):
            return reverse_lazy('company:profile-company', kwargs={'pk': self.object.company.id})

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)    


@method_decorator(Check_Role, name='dispatch')
class UpdateEmploye(UpdateView):
      model = models.Employee
      form_class = forms.Employee
      template_name = "company/employee/update-employee.html"  # Tu plantilla personalizada
      context_object_name = "employee" 

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.get(is_active=True,  employee=self.object)
            return context


      def form_valid(self, form):

            user = User.objects.get(employee_profile=self.object)
            # Establecer la clave del usuario
            user.username = form.instance.email
            user.save()
            form.instance.user = user
            form.instance.company = models.Company.objects.get(is_active=True, employee=self.object)

            # Comprobar si el rol ha cambiado a 'representante'
            if form.instance.role == 'representante':
                    # Verificar si ya existe otro empleado con el rol 'representante' en la misma empresa
                    existing_representative = models.Employee.objects.filter(company=form.instance.company, role='representante').exclude(id=form.instance.id).first()
                    if existing_representative:
                              messages.error('Solo puede haber un representante por empresa.')
                              return self.form_invalid(form)

            form.save()
            return super().form_valid(form)

      def get_success_url(self):
            return reverse_lazy('company:profile-company', kwargs={'pk': self.object.company.id})
      
      def logout_view(self, request):
            logout(request)  # Cierra la sesión del usuario actual
            return redirect('company:logins') 
                  
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)    

def Employee_Login(request):
      if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                  # Validar si el usuario está asociado con un empleado activo
                  if hasattr(user, 'employee_profile') and user.employee_profile.is_active:
                        login(request, user)
                        return redirect("food:dashboard")  # Redirigir al dashboard u otra vista
                  else:
                        messages.error(request, "No tienes permisos para iniciar sesión. Contacta al administrador.")
            else:
                  messages.error(request, "Nombre de usuario o contraseña incorrectos.")
      return render(request, "company/login/logins.html")



class Menu(ListView):
      model = models.Menu
      template_name = "company/menu/menu.html"
      context_object_name = 'menus'  # Esto cambiará el nombre del contexto de la lista de menús

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # context['services'] = models.Service.objects.filter(company=self.request.user.employee_profile.company)  # Filtrar los servicios por la compañía activa
            # Obtener la compañía activa (solo una)
            # context['categoria'] = models.Category.objects.filter()  # Filtrar las categorías por la compañía activa
            company = models.Company.objects.get(is_active=True, employee=self.request.user.employee_profile)
            context['company'] = company
            context['menus'] = models.Menu.objects.filter(company=self.request.user.employee_profile.company) 
            context['contrato'] = models.Contract.objects.get(company=company, is_active=True) if models.Contract.objects.filter(company=company, is_active=True).exists() else None
            context['menus_choices'] = models.MenuChoices.objects.filter(company=company)
            
            return context

      def post(self, request, *args, **kwargs):
            # Obtener los IDs seleccionados enviados como JSON
            selected_ids = request.POST.get('selected_ids')
            
            if selected_ids:
                  try:
                        # Convertir el JSON a una lista de IDs
                        selected_ids = json.loads(selected_ids)
                  except json.JSONDecodeError:
                        return JsonResponse({"error": "Formato de IDs inválido."}, status=400)

                  # Iterar por cada ID y crear un registro en MenuChoices
                  deleted_count, _ = models.MenuChoices.objects.filter(company=request.user.employee_profile.company).delete()
                  for menu_id in selected_ids:
                        menu = get_object_or_404(models.Category, id=menu_id)
                        models.MenuChoices.objects.create(menu=menu, company=request.user.employee_profile.company)

            else:
                    menus_selected = request.POST.getlist('menus')  # Menús seleccionados
                    all_menus = models.MenuChoices.objects.filter(company=self.request.user.employee_profile.company)  # Todos los menús relacionados
                    for menu in all_menus:
                              if str(menu.id) in menus_selected:  # Si el menú está seleccionado
                                      role = request.POST.get(f'role_{menu.id}')
                                      menu.role = role
                              menu.save()

            return redirect(reverse('company:menu'))


class MenuSelect(DetailView):
      model = models.MenuChoices
      template_name =  "company/menu/menu-select.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
      #       company = models.Company.objects.get(is_active=True, employee=self.request.user.employee_profile) 
            context['platos'] = models.Category.objects.get(id=self.object.menu.id)
            return context          
      
class CreateCategoryForCompany(CreateView):
      model = models.Category
      form_class = forms.Category
      template_name = "company/menu/create-category-for-company.html"
      success_url = reverse_lazy('company:menu')  # Red


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            company = models.Company.objects.get(is_active=True, employee=self.request.user.employee_profile)
            context['company'] = company
            context['service'] = models.Service.objects.get(id=self.kwargs.get('pk')) 
            context['menu_choices'] = models.MenuChoices.objects.filter(company=company)

            return context          

      def form_valid(self, form):
            company = models.Company.objects.get(is_active=True, employee=self.request.user.employee_profile)
            form.instance.company = company
            return super().form_valid(form)

class SelectMenu(DetailView):
      model = models.Menu
      template_name = "company/menu/select-menu.html"
      context_object_name = 'menu'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            company = models.Company.objects.get(is_active=True, employee=self.request.user.employee_profile)
            context['platos'] = models.Plato.objects.filter(menu=self.object)  # Filtrar los platos por el menú seleccionado
            context['company'] = company
            context['orders'] = models.Order.objects.filter(employee=self.request.user.employee_profile, company=company)  # Filtrar las órdenes
            return context

      def post(self, request, *args, **kwargs):
            # Obtener los platos seleccionados desde el formulario (IDs de platos seleccionados)
            platos_select = self.request.POST.getlist('plato')  # Usamos `getlist` para obtener múltiples valores
            for id_plato in platos_select:
                        plato= models.Plato.objects.get(id=int(id_plato))  
                        models.Order.objects.create(
                              employee=self.request.user.employee_profile, 
                              company=self.request.user.employee_profile.company,  # Asignar la compañía del empleado
                              plato=plato, 
                              status='pendiente'
                        )
            return redirect(reverse('company:orders'))


# Menu , Ordenes, Repodes y mas
class OrderReport(TemplateView):
      model = models.Order
      # form_class = forms.Employee
      template_name = "company/order/order-report.html"  # Tu plantilla personalizada
      context_object_name = "employee" 

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['orders'] = models.Order.objects.filter(employee=self.request.user.employee_profile, company=company)
            return context


class Orders(TemplateView):
      model = models.Order
      template_name = "company/order/orders.html"
      context_object_name = "employee"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            orders = models.Order.objects.filter(employee=self.request.user.employee_profile)
            move = models.Movements.objects.filter(employee=self.request.user.employee_profile)

            status = self.request.GET.get('status')
            if status:
                    orders = orders.filter(status=status)
            
            context['orders'] = orders  # Pasar los pedidos filtrados al contexto
            context['move'] = move
       
            return context




class AllOrders(TemplateView):
      model = models.Order
      template_name = "company/order/all-orders.html"
      context_object_name = "employee"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            category_id = self.request.GET.get('category')
            company_id = self.request.GET.get('company')
            status = self.request.GET.get('status')
            
            orders = models.Order.objects.filter(status='pendiente')
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
                        orders_company__status__in=['pendiente', ]
            ).distinct()
            context['categories'] = models.Category.objects.all()
            return context
      

      def post(self, request):
            # Obtener los platos seleccionados desde el formulario (IDs de platos seleccionados)
            if request.POST.getlist('ids[]'):
                  orders = models.Order.objects.filter(id__in=request.POST.getlist('ids[]'))
                  for order in orders:
                        order.status = 'preparando'
                        order.save()
            return redirect(reverse('company:all-orders'))


class EnviarOrder(TemplateView):
      template_name = "company/order/enviar-order.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # orders = models.Order.objects.filter(company= company, status='pendiente')
            # context['company'] =  models.Company.objects.filter(
            #             is_active=True, orders_company__status='enviado')

            orders = models.Order.objects.filter(status='enviado')
            orders_by_company = {}
            for order in orders:
                    company_name = order.company.name
                    company_img = order.company.img.url if order.company.img else None
                    company_id =order.company.id
                    if company_name not in orders_by_company:
                              orders_by_company[company_name] = {
                                      'orders': [],
                                      'img': company_img,
                                      'id': company_id,
                              }
                    orders_by_company[company_name]['orders'].append(order)

            context['company'] = orders_by_company  # Pass the grouped orders to the context
            # context['orders'] = orders
            # context['total'] = sum(order.plato.price for order in orders)
            return context


class RealizeOrderCompany(TemplateView):
      model = models.Company
      template_name = "company/order/realize-order-company.html"
      context_object_name = "company"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            company = models.Company.objects.get(id=self.kwargs['pk'])
            orders = models.Order.objects.filter(company= company, status='enviado')
            context['total'] = sum(order.price for order in orders)
            context['company'] = company
            context['orders'] = orders
            return context

      # Obtener las órdenes pendientes de la compañía
      def post(self, request, *args, **kwargs):
            orders = models.Order.objects.filter(company__id= self.kwargs['pk'], status='enviado')
            company = models.Company.objects.get(id=self.kwargs['pk'])
            company.total_to_pay +=  sum(order.price for order in orders)
            company.save()
            models.Movements(
                  mount = sum(order.price for order in orders),
                  description= company.name + 'Ingreso por ordenes total de ordenes' + str(orders.count()), 
            )
            for order in orders:
                  order.status = 'entregado'
                  order.save()
                  models.Movements(
                        name = order.name,
                        company= company,
                        employee= order.employee,
                        mount= order.price,
                        date= datetime.now(),
                        type_move='ingreso',
                  ).save()
     
            return redirect(reverse('company:enviar-order'))
      



class Report(TemplateView):
      template_name = "company/finance/report.html"
      context_object_name = 'companys'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            start_month = self.request.GET.get('start_month')
            end_month = self.request.GET.get('end_month')
            move = models.Movements.objects.all()

            if start_month and end_month:
                  start_date = datetime(datetime.now().year, int(start_month), 1)
                  end_date = datetime(datetime.now().year, int(end_month), calendar.monthrange(datetime.now().year, int(end_month))[1])
                  move = move.filter(date__range=(start_date, end_date))

            orders_pendiente = models.Order.objects.filter(status='entregado')
            context['movements'] = move
            context['total'] = sum(mount.mount for mount in move)
            context['total_pendiente'] = sum(order.plato.price for order in orders_pendiente)
            return context







class Claims(TemplateView):
      model = models.Claim
      template_name = "company/claims/claims.html"
      # success_url = reverse_lazy('claim_list')  # Redirige a una lista de reclamaciones

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['claims'] = models.Claim.objects.filter( status='pending',  employee=self.request.user.employee_profile) 
            return context

      def form_valid(self, form):
            # Asigna automáticamente la compañía y el empleado logueado
            form.instance.company = self.request.user.employee_profile.company
            form.instance.employee = self.request.user.employee_profile
            return super().form_valid(form)


class CreateClaim(CreateView):
      model = models.Claim
      form_class = forms.Claim
      template_name = "company/claims/create-claim.html"
      success_url = reverse_lazy('company:claims')  # Redirige a la lista de reclamaciones

      def form_valid(self, form):
            # Asigna automáticamente la compañía y el empleado logueado
            form.instance.company = self.request.user.employee_profile.company
            form.instance.employee = self.request.user.employee_profile
            return super().form_valid(form)

# Vista para actualizar una reclamación
class UpdateClaim(UpdateView):
      model = models.Claim
      form_class = forms.Claim
      template_name = "company/claims/update-claim.html"
      success_url = reverse_lazy('company:claims')  # Redirige a la lista de reclamaciones

      def form_valid(self, form):
            # Asigna automáticamente la compañía y el empleado logueado
            form.instance.company = self.request.user.employee_profile.company
            form.instance.employee = self.request.user.employee_profile
            return super().form_valid(form)




# Contratos 


class Contratos(TemplateView):
      template_name = "company/contratos/contratos.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['contratos'] = models.Contract.objects.all()
            return context

class ContratosCompany(TemplateView):
      template_name = "company/contratos/contratos-company.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['contratos'] = models.Contract.objects.filter(company_id=self.kwargs['pk'])
            context['company'] = models.Company.objects.get(id=self.kwargs['pk'])
            return context

class CreateContrato(CreateView):
      template_name = "company/contratos/create-contrato.html"
      model = models.Contract
      form_class = forms.Contract
      # success_url = reverse_lazy('company:contratos')


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] = models.Company.objects.get(id=self.kwargs['pk'])
            return context

      def form_valid(self, form):
            company = models.Company.objects.get(id=self.kwargs['pk'])
            form.instance.company = company
            form.instance.is_active = True
            # Guardar el formulario, pero sin guardar aún el campo ManyToMany
            form.save(commit=False)
            selected_services = self.request.POST.getlist('service_type')  
            # Limpiar los servicios existentes

            for contract in company.contracts.all():
                  contract.is_active = False
                  contract.save()

            company.services.clear()
            deleted_count, _ = models.MenuChoices.objects.filter(company=company).delete()
            for service_id in selected_services:
                  service = models.Service.objects.get(id=service_id)
                  company.services.add(service)

            company.save()
            print('Servicios seleccionados:', company.name)
            # Agrega lógica adicional aquí si es necesario
            return super().form_valid(form)
      
      def form_invalid(self, form):
            print(form.errors)  # Debugging purposes
            return super().form_invalid(form)

      def get_success_url(self):
            return reverse_lazy('company:profile-company', kwargs={'pk': self.object.company.id})
      

class UpdateContrato(UpdateView):
      template_name = "company/contratos/update-contrato.html"
      model = models.Contract
      form_class = forms.Contract


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] = models.Company.objects.get(id=self.object.company.id)
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      def get_success_url(self):
            return reverse_lazy('company:admin-company')



class DetailContrato(DetailView):
      template_name = "company/contratos/detail-contrato.html"
      model = models.Contract
      context_object_name = 'contrato'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context



# Restaurante
class Platos(TemplateView):
      template_name = "company/platos/platos.html"

            # context['categorias'] = models.Category.objects.all()
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            # Obtener el filtro de categoría (si existe)
            categoria_id = self.request.GET.get('categoria')
            print(categoria_id)
            if categoria_id:
                  context['platos'] = models.Plato.objects.filter(category_id=int(categoria_id))
                  context['categoria_show'] = models.Category.objects.get(pk=int(categoria_id))
            else:
                  context['platos'] = models.Plato.objects.all()

            context['categorias'] = models.Category.objects.all()
            print(models.Category.objects.all())
            return context



class CreatePlato(CreateView):
      template_name = "company/platos/create-plato.html"
      model = models.Plato
      form_class = forms.Plato
      success_url = reverse_lazy('company:platos')


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)  # Imprime los errores del formulario
            return super().form_invalid(form)
      


class UpdatePlato(UpdateView):
      template_name = "company/platos/update-plato.html"
      model = models.Plato
      form_class = forms.Plato
      success_url = reverse_lazy('company:platos')


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)  # Imprime los errores del formulario
            return super().form_invalid(form)
      

class PlatoDetail(DetailView):
      model = models.Plato
      template_name = "company/platos/plato-detail.html"
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['exist_order'] = models.Order.objects.filter(          
                  employee=self.request.user.employee_profile, 
                  company=self.request.user.employee_profile.company,  
                  status__in=['pendiente', 'preparando', 'enviado']
                  ).exists()
            return context

      
      def post(self, request, *args, **kwargs):
            plato= self.get_object()  
            models.Order.objects.create(
                  employee=self.request.user.employee_profile, 
                  company=self.request.user.employee_profile.company,  
                  name= plato.name, price = plato.price,  img= plato.img, status='pendiente'
            ).save()
            return redirect(reverse('company:orders'))



class DesactivarPlato(View):
      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect('login')  # Redirige al login si el usuario no está autenticado

            # Obtener y eliminar el objeto
            plato = get_object_or_404(models.Plato, id=self.kwargs['pk'])
            if plato.is_active:  # Si el plato está activo, lo desactiva
                  plato.is_active = False
            else:  # Si el plato está desactivado, lo activa
                  plato.is_active = True
            plato.save()

        # Redirigir al success_url
            return redirect(reverse_lazy('company:platos'))
      

class CreateCategory(CreateView):
      template_name = "company/platos/create-category.html"
      model = models.Category
      form_class = forms.Category
      success_url = reverse_lazy('company:platos')

      def form_valid(self, form):
            form.instance.user = self.request.user
            form.instance.is_active = True
            return super().form_valid(form)
      
class UpdateCategory(UpdateView):
      template_name = "company/platos/update-category.html"
      model = models.Category
      form_class = forms.Category
      success_url = reverse_lazy('company:platos')

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      

# Recuperar usuario
class RecoveryPassword(TemplateView):
      template_name = "company/recovery/recovery-password.html"
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context 

      def post(self, request, *args, **kwargs):
            email = request.POST.get('email')
            code = request.POST.get('code')
            print(email, code)
            if email:
                  user = get_object_or_404(User, username=email)
                  code = random.randint(1000,  1999)
                  employe = models.Employee.objects.get(user=user)
                  employe.code = code
                  employe.save()
                  send_mail(
                              'Código de recuperación',
                              f'Tu código de recuperación es: {code}',
                              'untal.wandy@gmail.com',
                              [email],
                              fail_silently=False,
                        )

                  context = self.get_context_data(**kwargs)
                  context['email'] = email
                  messages.success(request, f'Se ha enviado un código de recuperación a {email}.')
                  return render(request, self.template_name, context)

            if code:
                  email_send = request.POST.get('email_send')
                  user = get_object_or_404(User, username=email_send)
                  if  user.employee_profile.code == code:
                        context = self.get_context_data(**kwargs)
                        context['verify'] = True
                        context['email_send2'] = email_send
                        messages.success(request, f' Codigo verificado correctamente.')
                        return render(request, self.template_name, context)
                  else:
                        messages.error(request, 'Código incorrecto. Inténtalo de nuevo.')
                        return redirect('company:recovery-password')

            if request.POST.get('new_password'):
                  email_send2 = request.POST.get('email_2')
                  user = get_object_or_404(User, username=email_send2)
                  password = request.POST.get('new_password')
                  user.set_password(password)
                  user.save()
                  messages.success(request, 'Contraseña actualizada correctamente.')
                  return redirect('company:logins')



class VerifyCode(TemplateView):
      template_name = "company/recovery/verify-code.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def post(self, request, *args, **kwargs):
            code = request.POST.get('code')
            # Aquí deberías verificar el código con el que se envió al correo electrónico
            # Esto es solo un ejemplo, deberías implementar la lógica de verificación de código
            if code == "1234":  # Reemplaza esto con la lógica real de verificación
                  messages.success(request, 'Código verificado correctamente. Ahora puedes cambiar tu contraseña.')
                  return redirect('company:reset-password')
            else:
                  messages.error(request, 'Código incorrecto. Inténtalo de nuevo.')
                  return redirect('company:verify-code')

class MyProfile(TemplateView):
      template_name = "company/profile/my-profile.html"
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context


class DeleteAccount(DeleteView):
      template_name = "company/profile/delete-account.html"
      model = User
      success_url = reverse_lazy('company:logins')

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)  # Imprime los errores del formulario
            return super().form_invalid(form)




class CreateUser(CreateView):
      model = models.Employee
      form_class = forms.Employee
      template_name = "company/user/create-user.html"  # Tu plantilla personalizada

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
            
      def form_valid(self, form):
            form.instance.company = None
            form.instance.role = 'representante'
            form.instance.first_name  = 'Userio' + str(random.randint(0, 1000))
            form.instance.is_active = True
            user  = User(
                  username= form.instance.email,
                  email= form.instance.email,
            )
            # Establecer la clave del usuario
            password = form.instance.password # Reemplázalo por la clave que necesites
            user.set_password(password)
            user.save()
            
            form.instance.user = user
            form.save()
            return super().form_valid(form)

      def get_success_url(self):
            return reverse_lazy('company:create-company', kwargs={'pk': self.object.id})


def Logout(request):
      logout(request)
      return redirect('company:logins')


class ListCompany(ListView):
      model = models.Company
      template_name = "company/company/list-company.html"
      context_object_name = 'companys'  # Esto cambiará el nombre del contexto de la lista de menús

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['companys'] = models.Company.objects.filter(is_active=True)
            return context
      

class DeleteCompany(DeleteView):
      template_name = "company/company/delete-company.html"
      model = models.Company
      success_url = reverse_lazy('company:admin-company')

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      def form_invalid(self, form):
            print(form.errors)  # Imprime los errores del formulario
            return super().form_invalid(form)
      

class Profile(TemplateView):
      template_name = "company/profile/profile.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
      

class UpdateRestaurant(UpdateView):
      model = models.Restaurant
      form_class = forms.Restaurant
      template_name = "food/restaurant/update-restaurant.html"
      context_object_name = 'restaurant'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            restaurant = self.object  # Obtener la empresa actual
            return context

      def form_valid(self, form):
            return super().form_valid(form)

      def get_success_url(self):
            return reverse_lazy('company:restaurant-update' , kwargs={'pk': self.object.id})
      

class Facturacion(TemplateView):
      template_name = "company/facturacion/facturacion.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['list_companys'] = models.Company.objects.filter(is_active=True)
            if self.request.GET.get('company_id'):
                  context['company'] = models.Company.objects.get(id= int(self.request.GET.get('company_id')),
                  is_active=True)
            return context
      


class POS(TemplateView):
      template_name = "company/pos/pos.html"

      help = "Ayuda"
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
       
            return context
      
# Hola mundo
""" 
            Hola
"""