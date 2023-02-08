from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control form-control-lg text-center '
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control form-control-lg text-center '
        }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control form-control-lg  text-center '
        }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your email',
        'class': 'form-control form-control-lg  text-center '
        }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control form-control-lg text-center '
        }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        'class': 'form-control form-control-lg  text-center '
        }))