from django.contrib import admin
from Company.models import Company, Service, Employee, Menu, Order, Invoice, Payment, Plato, Claim, Contract, Category, GlobalMenu

admin.site.register(Company)
admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Plato)
admin.site.register(Claim) 

# Restaurante los modelos
admin.site.register(Category)  # Este modelo es para las categorias de los platos. 
admin.site.register(GlobalMenu)  # Este modelo es para los menús globales de la empresa.
admin.site.register(Contract)   # Este modelo es para las contrataciones de los empleados con los clientes. 


# Register your models here.