from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('username', 'first_name', 'last_name', 'password', 'email', 'telefone')
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PerfilForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    