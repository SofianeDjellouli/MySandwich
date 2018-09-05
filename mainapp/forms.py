from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FinProduit, Client, CarteBancaire

class FinProduitForm(forms.ModelForm):
    class Meta:
        model = FinProduit
        fields = '__all__'
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=
                             'Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['user']
        
class CarteBancaireForm(forms.ModelForm):
    class Meta:
        model = CarteBancaire
        exclude = ['user']