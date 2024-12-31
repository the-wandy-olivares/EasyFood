from django.contrib import admin
from Company.models import Company, Service, Employee, Menu, Order, Invoice, Payment, Plato, Claim, Contract, Category, GlobalMenu, MenuChoices, Restaurant

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
admin.site.register(MenuChoices)  # Este modelo es para las relaciones entre los menús y los platos.
admin.site.register(Restaurant)  # Este modelo es para los restaurantes 

# Register your models here.