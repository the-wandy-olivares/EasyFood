from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import json
from django.views.generic import TemplateView, View, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.db.models import Sum
from collections import defaultdict
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
import random

# http://127.0.0.1:8000/company/logins

# From my apps
from Company import models
from Company import forms



def Check_Role(view_func):
      def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                  if request.user.username != 'admin' or 'untalwandy':
                        if request.user.employee_profile.role == "ejecutivo":
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

                  
                  
@method_decorator(Check_Role, name='dispatch')
class AdminCompany(TemplateView):
      template_name = "company/admin-company.html"

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)    
            

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.filter(is_active=True)
            return context
    
@method_decorator(Check_Role, name='dispatch')
class CreateCompany(CreateView):
      model = models.Company
      form_class = forms.Company
      template_name = "company/create-company.html"  # Tu plantilla personalizada
      # success_url = reverse_lazy('company:admin')  # Redirige después de guardar

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.filter(is_active=True)
            return context
            
      def form_valid(self, form):            
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
            return reverse_lazy('company:profile-company', kwargs={'pk': self.object.id})


      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)    

@method_decorator(Check_Role, name='dispatch')

@method_decorator(login_required, name='dispatch')  # Asegurarse de que el usuario esté autenticado
class ProfileCompany(DetailView):
      model = models.Company
      form_class = forms.Company
      template_name = "company/profile-company.html"
      success_url = reverse_lazy('company:admin-company')  # Redirige después de guardar
      context_object_name = "company"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            company = self.object  # Obtener la empresa actual

            # Agrupar menús por día


            # Obtener empleados activos en la empresa
            context['employee'] = models.Employee.objects.filter(company=company)
            context['count'] = models.Employee.objects.filter(company=company, is_active=True).count()

            # Si necesitas un total de lo facturado o pendiente, puedes usar aggregates
            total_billed = company.invoices.aggregate(Sum('amount'))['amount__sum'] or 0
            total_paid = company.invoices.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
            context['total_billed'] = total_billed
            context['total_paid'] = total_paid
            context['total_pending'] = total_billed - total_paid  # Monto pendiente

            return context

      def form_valid(self, form):
            company = form.save()
            
            return super().form_valid(form)

      def get(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return redirect(reverse('company:logins'))
            return super().get(request, *args, **kwargs)


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

            user  = User.objects.get( employee_profile=self.object)
            # Establecer la clave del usuario
            user.username = form.instance.email
            password = form.instance.password # Reemplázalo por la clave que necesites
            user.set_password(password)
            user.save()
            form.instance.user = user
            form.instance.company = models.Company.objects.get(is_active=True,  employee=self.object)
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
            company = models.Company.objects.get(is_active=True, employee=self.request.user.employee_profile)# Devolver el primero que encuentre
            context['menus'] = models.Menu.objects.filter(company=self.request.user.employee_profile.company) 
            # context['categoria'] = models.Category.objects.filter()  # Filtrar las categorías por la compañía activa
            context['company'] = company
            
            return context

      def post(self, request, *args, **kwargs):
            # Obtener los IDs seleccionados enviados como JSON
            selected_ids = request.POST.get('selected_ids')
            
            if not selected_ids:
                  return JsonResponse({"error": "No se recibieron IDs."}, status=400)

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

            return redirect(reverse('food:restaurant'))





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

        # Obtener los filtros de la URL
        status_filter = self.request.GET.get('status', None)  # Filtro por estado (pendiente/completado)
        date_filter = self.request.GET.get('date', None)  # Filtro por fecha (formato YYYY-MM-DD)

        # Filtrar los pedidos según los criterios
        orders = models.Order.objects.filter(employee=self.request.user.employee_profile, company=self.request.user.employee_profile.company)

        # Filtrar por estado si se ha enviado el filtro
        if status_filter:
            orders = orders.filter(status=status_filter)

        # Filtrar por fecha si se ha enviado el filtro
        if date_filter:
            try:
                filter_date = timezone.datetime.strptime(date_filter, "%Y-%m-%d").date()
                orders = orders.filter(date__date=filter_date)
            except ValueError:
                pass  # Si el formato de fecha es incorrecto, no aplicar el filtro

        context['orders'] = orders  # Pasar los pedidos filtrados al contexto
        return context



@method_decorator(Check_Role, name='dispatch')
class AllOrders(TemplateView):
    model = models.Order
    template_name = "company/order/all-orders.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            # Obtener los filtros de la URL
            status_filter = self.request.GET.get('status', None)  # Filtro por estado (pendiente/completado)
            date_filter = self.request.GET.get('date', None)  # Filtro por fecha (formato YYYY-MM-DD)

            # Filtrar los pedidos según los criterios
            orders = models.Order.objects.filter(company=self.request.user.employee_profile.company)

            # Filtrar por estado si se ha enviado el filtro
            if status_filter:
                  orders = orders.filter(status=status_filter)

            # Filtrar por fecha si se ha enviado el filtro
            if date_filter:
                  try:
                        filter_date = timezone.datetime.strptime(date_filter, "%Y-%m-%d").date()
                        orders = orders.filter(date__date=filter_date)
                  except ValueError:
                        pass  # Si el formato de fecha es incorrecto, no aplicar el filtro

            context['orders'] = orders  # Pasar los pedidos filtrados al contexto
            return context



class Report(TemplateView):
      template_name = "company/finance/report.html"
      context_object_name = 'companys'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            # Obtener los filtros de la solicitud GET
            status = self.request.GET.get('status', '')
            employee_id = self.request.GET.get('employee', '')
            company_id = self.request.GET.get('company', '')
            start_date = self.request.GET.get('start_date')
            end_date = self.request.GET.get('end_date')

            # Obtener todas las órdenes completadas por defecto
            report = models.Order.objects.filter( company = self.request.user.employee_profile.company, status='completado' )

            # Aplicar filtros si existen
            if status:
                  report = report.filter(status=status)
            if start_date:
                        report = report.filter(date__gte=start_date)
                  
            if end_date:
                        report = report.filter(date__lte=end_date)

            # Crear datos del reporte financiero
            report_data = []
            companys = models.Company.objects.filter(is_active=True, employee=self.request.user.employee_profile)
            for company in companys:
                  total_billed = company.invoices.aggregate(Sum('amount'))['amount__sum'] or 0
                  total_paid = company.invoices.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
                  total_pending = total_billed - total_paid

                  report_data.append({
                  'company': company,
                  'total_billed': total_billed,
                  'total_paid': total_paid,
                  'total_pending': total_pending,
                  })

            # Pasar datos al contexto
            context['report'] = report
            context['companys'] = companys
            context['report_data'] = report_data
            context['employee'] = models.Employee.objects.filter(company=self.request.user.employee_profile.company)

            # Pasar filtros seleccionados para mantenerlos en el formulario
            context['status'] = status
            context['start_date'] = start_date
            context['end_date'] = end_date
            context['employee_id'] = employee_id
            context['company_id'] = company_id


            return context



class Claims(TemplateView):
      model = models.Claim
      template_name = "company/claims/claims.html"
      # success_url = reverse_lazy('claim_list')  # Redirige a una lista de reclamaciones

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['claims'] = models.Claim.objects.filter(company=self.request.user.employee_profile.company)
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
            return context

      def form_valid(self, form):
            company = models.Company.objects.get(id=self.kwargs['pk'])
            form.instance.company = company
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
      success_url = reverse_lazy('company:contratos')

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

      def get_success_url(self):
            return reverse_lazy('company:contratos')



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
            if email:
                  user = get_object_or_404(User, username=email)
                  code = user.employee_profile.code = random.randint(1000,  1999)
                  user.save()
                        # send_mail(
                        #       'Código de recuperación',
                        #       f'Tu código de recuperación es: {code}',
                        #       'untal.wandy@gmail.com',
                        #       [email],
                        #       fail_silently=False,
                        # )

                  context = self.get_context_data(**kwargs)
                  context['email'] = email
                  messages.success(request, f'Se ha enviado un código de recuperación a {email}.')
                  return render(request, self.template_name, context)

            if code:
                  pass





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



def Logout(request):
      logout(request)
      return redirect('company:logins')