from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'username',
        'class': 'form-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-input'
    }))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': "Ім'я", 'class': 'form-input'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': "Прізвище", 'class': 'form-input'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Username", 'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': "Email", 'class': 'form-input'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': "Пароль", 'class': 'form-input'})
    )
    password2 = forms.CharField(
        label="Підтвердіть пароль",
        widget=forms.PasswordInput(attrs={'placeholder': "Підтвердіть пароль", 'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "Ім'я"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Прізвище"}),
            'username': forms.TextInput(attrs={'placeholder': "Ім'я користувача"}),
            'email': forms.EmailInput(attrs={'placeholder': "Email"}),
        }