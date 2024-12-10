
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View, CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.db.models import Sum




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
      success_url = reverse_lazy('company:admin-company')  # Redirige después de guardar

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.filter(is_active=True)
            return context
            
      def form_valid(self, form):
            # Agrega lógica adicional aquí si es necesario
            return super().form_valid(form)

      def get_success_url(self):
            # Usamos self.object para acceder al objeto actualizado
            return reverse_lazy('company:profile-company', kwargs={'pk': self.object.id})


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
class ProfileCompany(DetailView):
      model = models.Company
      form_class = forms.Company
      template_name = "company/profile-company.html"  # Tu plantilla personalizada
      success_url = reverse_lazy('company:admin-company')  # Redirige después de guardar
      context_object_name = "company" 

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.get(is_active=True,  id=self.kwargs.get('pk'))
            context['employee'] = models.Employee.objects.filter(company=self.object, )
            context['count'] = models.Employee.objects.filter(company=self.object, is_active=True).count()
            return context
            
      def form_valid(self, form):
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
                  username= form.instance.username,
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


# Menu , Ordenes, Repodes y mas
class OrderReport(TemplateView):
      model = models.Order
      # form_class = forms.Employee
      template_name = "company/order/order-report.html"  # Tu plantilla personalizada
      context_object_name = "employee" 

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['orders'] = models.Order.objects.filter(employee__user=self.request.user)
            return context

@method_decorator(Check_Role, name='dispatch')
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
        orders = models.Order.objects.all()

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


class InvoiceReport(ListView):
      model = models.Company
      template_name = "company/finance/invoice-report.html"  
      context_object_name = 'companys'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Obtenemos los datos de las facturas y pagos
            report_data = []
            for company in context['companys']:
                  total_billed = company.invoices.aggregate(Sum('amount'))['amount__sum'] or 0
                  total_paid = company.invoices.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
                  total_pending = total_billed - total_paid

                  report_data.append({
                  'company': company,
                  'total_billed': total_billed,
                  'total_paid': total_paid,
                  'total_pending': total_pending,
                  })

            context['report_data'] = report_data
            return context