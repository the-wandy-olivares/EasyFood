from django import forms
from .models import Company

class Company(forms.ModelForm):
    class Meta:
        model = Company
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
            'representative': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter representative name'}),
            'services': forms.CheckboxSelectMultiple(),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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