
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DetailView
from Company import models
from Company import forms

class AdminCompany(TemplateView):
      template_name = "company/company-admin.html"

      def get(self, request, *args, **kwargs):
            # if not request.user.is_authenticated:
            #       return redirect(reverse('customer:search-company'))
            return super().get(request, *args, **kwargs)    
            

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['company'] =  models.Company.objects.filter(is_active=True)
            return context
    

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