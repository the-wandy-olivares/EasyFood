from django.contrib import admin
from Company.models import Company, Service, Employee, Menu, Order, Invoice, Payment, Plato, Claim

admin.site.register(Company)
admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Plato)
admin.site.register(Claim)  

# Register your models here.