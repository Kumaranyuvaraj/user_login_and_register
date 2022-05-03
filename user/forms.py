from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Code

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'email','phone_no','password1', 'password2']

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text='Enter SMS verification code')
    class Meta:
        model = Code
        fields = ('number',)


