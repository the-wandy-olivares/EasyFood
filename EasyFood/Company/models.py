from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
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
      representative = models.CharField(max_length=255, verbose_name="Principal reprentante", blank=True)
      services = models.ManyToManyField('Service', related_name='companies', verbose_name="Contracted Services", blank=True)
      is_active = models.BooleanField(default=True)

      class Meta:
            verbose_name = "Client Company"
            verbose_name_plural = "Client Companies"

      def __str__(self):
            return self.name


class Service(models.Model):
      name = models.CharField(max_length=50, choices=Company.SERVICE_OPTIONS, unique=True, blank=True)
      class Meta:
            verbose_name = "Service"
            verbose_name_plural = "Services"

      def __str__(self):
            return self.get_name_display()



class Employee(models.Model):
      ROLE_OPTIONS = [
                  ('ejecutivo', 'Ejecutivo'),
                  ('estandar', 'Estandar'),
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
      username = models.CharField(default='employee', max_length=80)
      password = models.CharField(max_length=100)
      first_name = models.CharField(max_length=255, verbose_name="Nombre", blank=True)
      last_name = models.CharField(max_length=255, verbose_name="Apellidos", blank=True)
      email = models.EmailField(unique=True, verbose_name="Correo electronico", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Numero de telefono", blank=True, null=True)
      role = models.CharField(max_length=10, choices=ROLE_OPTIONS, verbose_name="Role", blank=True)
      genero = models.CharField(max_length=10, choices=GENERO, verbose_name="Genero", blank=True)
      is_active = models.BooleanField(default=True, verbose_name="Estado activo", blank=True)

      class Meta:
            verbose_name = "Employee"
            verbose_name_plural = "Employees"

      def __str__(self):
            return f"{self.first_name} {self.last_name} - {self.company.name}"


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

      is_active = models.BooleanField(default=True)


      
      def __str__(self):
            return f"{self.get_day_display()} - {self.get_time_display()}"



# Modelo Plato que contiene el nombre, descripción y el plato relacionado con el menú
class Plato(models.Model):
      menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="platos_menu")
      name = models.CharField(max_length=100, verbose_name="Nombre del Plato")
      description = models.TextField(verbose_name="Descripción del Plato")

      is_active = models.BooleanField(default=True)
      
      def __str__(self):
            return f'{self.name} - {self.menu}'


class Order(models.Model):
      company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="orders_company", blank=True, null= True)
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="orders", blank=True)
      plato = models.ForeignKey(Plato, on_delete=models.CASCADE, blank=True, related_name='plato', default=1)  # Relacionado con el plato seleccionado
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