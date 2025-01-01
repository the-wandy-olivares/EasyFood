from django.db import models
from django.contrib.auth.models import User
import datetime

class Company(models.Model):
      restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='restaurant_company', blank=True, null=True)

      SERVICE_OPTIONS = [
            ('desayuno', 'Desayuno'),
            ('comida', 'Comida'),
            ('cena', 'Cena'),
      ]

      name = models.CharField(max_length=255, verbose_name="Nombre", blank=True)
      img = models.ImageField(upload_to='media/company/', null=True, blank=True)
      tax_id = models.CharField(max_length=50, unique=True, verbose_name="Tax ID", blank=True)
      address = models.TextField(verbose_name="Address", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Phone", blank=True)
      email = models.EmailField(verbose_name="Email Address", blank=True)


      date = models.DateTimeField(default=datetime.datetime(2024, 12, 3, 0, 0), auto_now_add=False)


      representative = models.CharField(max_length=255, verbose_name="Principal reprentante", blank=True)
      cargo_representante = models.CharField(max_length=255, verbose_name="Cargo del Representante", blank=True)
      contact_representante = models.CharField(max_length=255, verbose_name="Contacto del Representante", blank=True)
      dni = models.CharField(max_length=15, verbose_name="DNI", blank=True)


      services = models.ManyToManyField('Service', related_name='companies', verbose_name="Contracted Services", blank=True)
      is_active = models.BooleanField(default=True)

      class Meta:
            verbose_name = "Client Company"
            verbose_name_plural = "Client Companies"

      def __str__(self):
            return self.name


class Service(models.Model):
      name = models.CharField(max_length=50, choices=Company.SERVICE_OPTIONS, unique=True, blank=True)
      img = models.ImageField(upload_to='media/service/', null=True, blank=True)
      description = models.TextField(verbose_name="Description", blank=True)
      class Meta:
            verbose_name = "Service"
            verbose_name_plural = "Services"

      def __str__(self):
            return self.get_name_display()



class Employee(models.Model):
      ROLE_OPTIONS = [
                  ('ejecutivo', 'Ejecutivo'),
                  ('estandar', 'Estandar'),
                  ('representante', 'Representante',)
      ]
      GENERO = [
                  ('masculino', 'Masculino'),
                  ('femenino', 'Femenino'),
      ]

      user = models.OneToOneField(
            User, 
            on_delete=models.CASCADE, 
            related_name='employee_profile',
            verbose_name="User", blank=True
      )
      
      company = models.ForeignKey( 'Company', on_delete=models.CASCADE, 
      related_name='employee', verbose_name='Company', blank=True)
      username = models.CharField(default='', max_length=80, blank=True)
      password = models.CharField(max_length=100, blank=True)
      first_name = models.CharField(max_length=255, verbose_name="Nombre", blank=True)
      last_name = models.CharField(max_length=255, verbose_name="Apellidos", blank=True)
      email = models.EmailField(unique=True, verbose_name="Correo electronico", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Numero de telefono", blank=True, null=True)
      role = models.CharField(max_length=15, choices=ROLE_OPTIONS, verbose_name="Role", blank=True)
      genero = models.CharField(max_length=10, choices=GENERO, verbose_name="Genero", blank=True)
      is_active = models.BooleanField(default=True, verbose_name="Estado activo", blank=True)
      code = models.CharField(max_length=10, verbose_name="Codigo de acceso", blank=True)
      class Meta:
            verbose_name = "Employee"
            verbose_name_plural = "Employees"

      def __str__(self):
            return f"{self.first_name} {self.last_name} "


class GlobalMenu(models.Model):

      # Opciones para los días de la semana
      DAY_CHOICES = [
      ('Lunes', 'Lunes'),
      ('Martes', 'Martes'),
      ('Miercoles', 'Miércoles'),
      ('Jueves', 'Jueves'),
      ('Viernes', 'Viernes'),
      ('Sabado', 'Sábado'),
      ('Domingo', 'Domingo'),
      ]

      # Opciones para los horarios
      TIME_CHOICES = [
      ('Desayuno', 'Desayuno'),
      ('Almuerzo', 'Almuerzo'),
      ('Cena', 'Cena'),
      ]


      day = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name="Día")
      time = models.CharField(max_length=20, choices=TIME_CHOICES, verbose_name="Horario")
      is_active = models.BooleanField(default=True)


      
      def __str__(self):
            return f"{self.get_day_display()} - {self.get_time_display()}"



# Modelo Menu que contiene el Día y el Horario
class Menu(models.Model):
      # Opciones para los días de la semana
      DAY_CHOICES = [
      ('Lunes', 'Lunes'),
      ('Martes', 'Martes'),
      ('Miercoles', 'Miércoles'),
      ('Jueves', 'Jueves'),
      ('Viernes', 'Viernes'),
      ('Sabado', 'Sábado'),
      ('Domingo', 'Domingo'),
      ]

      # Opciones para los horarios
      TIME_CHOICES = [
      ('Desayuno', 'Desayuno'),
      ('Almuerzo', 'Almuerzo'),
      ('Cena', 'Cena'),
      ]

      company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="menu_company")
      day = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name="Día")
      time = models.CharField(max_length=20, choices=TIME_CHOICES, verbose_name="Horario")
      img = models.ImageField(upload_to='media/menu/', null=True, blank=True)
      is_active = models.BooleanField(default=True)

      def __str__(self):
            return f"{self.get_day_display()} - {self.get_time_display()}"




class Category(models.Model):
      service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name="categories_service", blank=True, null=True) 
      name = models.CharField(max_length=50, verbose_name="Categoría del Plato")
      description = models.TextField(verbose_name="Descripción de la Categoría", blank=True, null=True)
      img = models.ImageField(upload_to='media/category/', null=True, blank=True)
      is_active = models.BooleanField(default=True)

      # Relacionado con la empresa seleccionada
      is_company = models.BooleanField(default=False)
      company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="categories_company", blank=True, null=True)

      def __str__(self):
            return self.name
      




""" 
            *Los menus son categorías, lo que sucede es que se hicieron unas modificaciones a como se manejan los menus sorry si no he resuelto esto, les juro que es un error mio y estoy consciente, per es facil de enternder los menus del templates son categorias y cada plato esta relacionado con la categoría (Menu) 
"""




class MenuChoices(models.Model):
      ROLE_OPTIONS = [
                  ('ejecutivo', 'Ejecutivo'),
                  ('estandar', 'Estandar'),
      ]

      menu = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="choices_menu", blank=True, null=True)
      company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="choices_company", blank=True, null=True) 
      role = models.CharField(max_length=10, choices=ROLE_OPTIONS, verbose_name="Role", blank=True, default='estandar')

      is_active = models.BooleanField(default=True)


      def __str__(self):
            return f"{self.company.name} - {self.menu.name}"




# Modelo Plato que contiene el nombre, descripción y el plato relacionado con el menú
class Plato(models.Model):
      menu = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="platos_menu", blank=True, null=True)  # Relacionado con el menú seleccionado
      name = models.CharField(max_length=100, verbose_name="Nombre del Plato")
      description = models.TextField(verbose_name="Descripción del Plato")
      price = models.IntegerField(verbose_name="Precio del Plato",default=0, blank=True)
      img = models.ImageField(upload_to='media/plato/', null=True, blank=True)  
      img1 = models.ImageField(upload_to='media/plato/', null=True, blank=True)  
      img2= models.ImageField(upload_to='media/plato/', null=True, blank=True)  
      
      # Imagen del plato
      category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="platos_category", blank=True, null=True, default=None)  # Relacionado con la categoría seleccionada
      is_active = models.BooleanField(default=True)
      
      def __str__(self):
            return f'{self.name} - {self.menu}'


class Order(models.Model):
      company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="orders_company", blank=True, null= True)
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="orders", blank=True, null=True)
      plato = models.ForeignKey(Plato, on_delete=models.CASCADE, blank=True, related_name='plato', default=1)  # Relacionado con el plato seleccionado

      name = models.CharField(max_length=255, verbose_name="Nombre del Plato", blank=True)
      price = models.IntegerField(default=0, verbose_name="Precio del Plato", blank=True)
      img = models.ImageField(upload_to='media/order/', null=True, blank=True)

      date = models.DateTimeField(auto_now_add=True)  # Fecha y hora del pedido
      status = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')], default='pendiente')



      class Meta:
            verbose_name = "Pedido"
            verbose_name_plural = "Pedidos"

      def __str__(self):
            return f"{self.employee} - {self.plato} - {self.date}"


# Consultar montos facturados y pagos pendientes
class Invoice(models.Model):
      company = models.ForeignKey(Company, related_name='invoices', on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      date_issued = models.DateField()
      due_date = models.DateField()
      paid = models.BooleanField(default=False)
      payment_date = models.DateField(null=True, blank=True)

      def __str__(self):
            return f"Invoice {self.id} - {self.company.name}"


class Payment(models.Model):
      invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      payment_date = models.DateField()

      def __str__(self):
            return f"Payment for Invoice {self.invoice.id}"


# Reclamaciones y solicitudes de cambios
class Claim(models.Model):
      company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="claims")
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="claims")
      order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="claims", null=True, blank=True)
      title = models.CharField(max_length=255)
      description = models.TextField()
      date_submitted = models.DateTimeField(auto_now_add=True)
      status = models.CharField(
            max_length=20, 
            choices=[('pending', 'Pendiente'), ('reviewed', 'Revisado'), ('resolved', 'Resuelto')],
            default='pending'
      )

      def __str__(self):
            return f"Reclamación: {self.title} - {self.status}"



class Contract(models.Model):
      company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contracts", verbose_name="Cliente", blank=True, null=True)
      service_type = models.ManyToManyField(Service, verbose_name="Tipo de Servicio")

      number_contract = models.CharField(max_length=100, verbose_name="Número de Contrato", default='', blank=True, null=True)

      delivery_schedule = models.TimeField(verbose_name="Horario de Entrega", blank=True, null=True)
      payment_terms = models.TextField(verbose_name="Términos de Pago")
      start_date = models.DateField(verbose_name="Fecha de Inicio")
      end_date = models.DateField(verbose_name="Fecha de Fin")
      is_active = models.BooleanField(default=True, verbose_name="Activo")
      observaciones = models.TextField(verbose_name="Observaciones", blank=True)



      def __str__(self):
            return f"Contrato con {self.company.name} - {self.service_type}"
      

class Restaurant(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant', verbose_name="Usuario", blank=True, null=True)
      name = models.CharField(max_length=255, default='', verbose_name="Nombre del Restaurante", blank=True, null=True)
      img = models.ImageField(upload_to='media/restaurant/', null=True, blank=True)
      address = models.TextField(verbose_name="Dirección", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Teléfono", blank=True)
      email = models.EmailField(verbose_name="Correo Electrónico", blank=True)
      is_active = models.BooleanField(default=True, verbose_name="Activo")
      date = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return self.name
      