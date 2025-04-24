from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


#Personalizar Formulario de Admin para mejor control
class UserCreationForm(forms.ModelForm):
    """Formulario para crear nuevos usuarios en el admin con doble verificación de contraseña."""
    password1 = forms.CharField(label='Contraseña',
                                widget=forms.PasswordInput,
                                help_text="Debe contener al menos 8 caracteres."
                                )
    password2 = forms.CharField(label='Confirmar Contraseña',
                                widget=forms.PasswordInput,
                                help_text="Debe contener al menos 8 caracteres.",
                                required=True
                                )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_type')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()  # <-- Guarda primero el usuario siempre (asigna ID)

        if commit:
            self.save_m2m()  # <-- ahora sí guarda M2M después de guardar el usuario

        return user


class UserChangeForm(forms.ModelForm):
    """Formulario para actualizar usuarios en el admin."""
    password = ReadOnlyPasswordHashField(label="Contraseña (ya hasheada)")

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'password',
            'profile_type', 'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )

    def clean_password(self):
        # Django exige esto para mantener la contraseña anterior intacta
        return self.initial["password"]