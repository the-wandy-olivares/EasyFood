from django import forms
from Company import models

class Company(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = [
            'name',
            'tax_id',  'address',
            'phone',  'email', 'representative',
            'services', 'is_active', 'img', 'cargo_representante', 'contact_representante',
            'dni', 
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de compañia'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RNC'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Direccion ejemplo: Santo Domingo, Santo Domingo Este, Calle Mendoza '}),

            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero de telefono de la empresa'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),

            'representative': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del representante'}),
            'contact_representante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacto del reprentante'}),
            'cargo_representante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo del representante'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI del representante'}),


            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-select-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'img': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input d-none' ,  # Personaliza el estilo si es necesario
            }),
        }
        labels = {
            'name': 'Nombre de compania',
            'tax_id': 'RNC',
            'address': 'Direccion ejemplo: Santo Domingo, Santo Domingo Este, Calle Mendoza ',
            'phone': 'Numero de telefono',
            'email': 'Correo',
            'representative': 'Descripcion',
            'services': 'Servicios de contrato',
            'is_active': 'Vigente',
        }



class Employee(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            'user',
            'company',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'is_active',
            'username',
            'genero',
            'password',
        ]
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control', 
            }),
            'company': forms.Select(attrs={
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Correo electronico'
            }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero de telefono'}),
            'role': forms.Select(attrs={'class': 'form-control'}),     
            
                    'genero': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class Order(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['plato']  # Solo necesitamos el campo plato
        widgets = {
            'plato': forms.CheckboxSelectMultiple,  # Para permitir múltiples selecciones de platos
        }

    # Opcional: para añadir una validación o lógica personalizada
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plato'].queryset = models.Plato.objects.all()


class Claim(forms.ModelForm):
    class Meta:
        model = models.Claim
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: "Retraso en la entrega del pedido" '
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la reclamación (opcional)',
            }),
            'order': forms.Select(attrs={
                'class': 'form-control',
            }),
        }




def generate_time_choices():
    times = []
    for hour in range(24):  # De 0 a 23 horas
        for minute in (0, 30):  # Minutos: 0 y 30
            time_str_24 = f"{hour:02}:{minute:02}"  # Formato 24 horas (HH:MM)
            time_str_12 = f"{hour % 12 or 12}:{minute:02} {'AM' if hour < 12 else 'PM'}"  # Formato 12 horas (HH:MM AM/PM)
            times.append((time_str_24, time_str_12))
    return times


class Contract(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = ['company', 'service_type', 'delivery_schedule', 'payment_terms', 'start_date', 'end_date', 'is_active', 'firma_resturant', 'firma_company']
        widgets = {
            'company': forms.Select(attrs={ 'placeholder': 'Seleccione el cliente'}),
            'delivery_schedule': forms.Select(
                            choices=generate_time_choices(),  # Opciones generadas dinámicamente
                            attrs={'class': 'form-control'}
                        ),

            'service_type': forms.CheckboxSelectMultiple(
                choices=[
                    ('desayuno', 'Desayuno'),
                    ('comida', 'Comida'),
                    ('cena', 'Cena'),
                ],
                attrs={ 'class': 'form-check-input' }
            ),
            # 'service_type': forms.CheckboxSelectMultiple(
            #     # choices=[  # Aquí defines las opciones de los checkboxes
            #     #     ('basic', 'Básico'),
            #     #     ('premium', 'Premium'),
            #     #     ('enterprise', 'Empresarial'),
            #     # ],
            #     attrs={ 'class': 'form-check-input' }
            # ),


            'payment_terms': forms.Textarea(attrs={ 'placeholder': 'Ingrese los términos de pago'}),
            'start_date': forms.DateInput(attrs={ 'placeholder': 'AAAA-MM-DD', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={ 'placeholder': 'AAAA-MM-DD', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class Category(forms.ModelForm):
        class Meta:
            model = models.Category
            fields = ['service', 'name', 'description', 'img', 'is_active' ]
            widgets = {
                'service': forms.Select(attrs={'class': 'form-control'}),
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Nombre'}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalles del menu ejemplo: Incluye nuestros mejores platos', 'rows': 3}),
                'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }


class Plato(forms.ModelForm):
    class Meta:
        model = models.Plato
        fields = ['menu', 'name', 'description', 'price', 'img', 'category', 'is_active']
        widgets = {
            'menu': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del plato'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del plato',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class Restaurant(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            'user', 'name', 'tax_id', 'img', 'address', 'phone', 'email', 'is_active'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Restaurante'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tax ID'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo '}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }