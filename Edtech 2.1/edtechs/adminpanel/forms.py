from socket import fromshare
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import  TextInput, EmailInput,PasswordInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control"
                }),
              'email': EmailInput(attrs={
                'class': "form-control"
                }),
             'password1': TextInput(attrs={
                'class': "form-control"
                }),
            'password2': TextInput(attrs={
                'class': "form-control"
                })
          
        }
        
        def __init__(self, *args, **kwargs):
            super(CreateUserForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'