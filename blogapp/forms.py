from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from django import forms


class PasswordInput(forms.PasswordInput):
    input_type='password'

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username','email','password')
        widgets = {'password':forms.PasswordInput()}
    
    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        user = User.objects.create_user(username=username,email=email,password=password)        
        
        user.save()        
        
        