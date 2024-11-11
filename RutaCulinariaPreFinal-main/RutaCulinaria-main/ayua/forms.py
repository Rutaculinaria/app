from django import forms
from django.core.exceptions import ValidationError
from .models import Orden, Plato
from datetime import date, time


class ClienteRegistroForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    telefono = forms.CharField(max_length=12, label="Número de Teléfono")

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError("Las contraseñas no coinciden.")
        return password_confirmation

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class OrdenForm(forms.ModelForm):
    fecha_retiro = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    hora_retiro = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Orden
        fields = ['cantidad', 'fecha_retiro', 'hora_retiro']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fecha_retiro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_retiro': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean_fecha_retiro(self):
        """
        Validar que la fecha de retiro no sea en el pasado.
        """
        fecha_retiro = self.cleaned_data.get('fecha_retiro')
        if fecha_retiro < date.today():
            raise forms.ValidationError("La fecha de retiro no puede ser en el pasado.")
        return fecha_retiro

    def clean_hora_retiro(self):
        """
        Validar que la hora de retiro esté entre las 10:00 AM y las 10:00 PM.
        """
        hora_retiro = self.cleaned_data.get('hora_retiro')
        if hora_retiro < time(10, 0) or hora_retiro > time(22, 0):
            raise forms.ValidationError("La hora de retiro debe estar entre las 10:00 y las 22:00.")
        return hora_retiro