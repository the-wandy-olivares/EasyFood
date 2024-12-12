from django import forms
from Company import models

class Company(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = [
            'name',
            'tax_id',  'address',
            'phone',  'email', 'representative',
            'services', 'is_active', 'img'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de compania'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RNC'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Direccion ejemplo: Santo Domingo, Santo Domingo Este, Calle Mendoza '}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero de telefono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'representative': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representante'}),
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
                'placeholder': 'username',
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
                'placeholder': 'Ejemplo: "Retraso en la entrega del pedido" '
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'El pedido #3722 estaba programado para entregarse el 10/12/24, pero aún no he recibido el producto',

            }),
            'order': forms.Select(attrs={

            }),
        }