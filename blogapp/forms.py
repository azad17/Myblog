from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets
from django import conf, forms
import string

class PasswordInput(forms.PasswordInput):
    input_type='password'

class UserForm(ModelForm):
    confirm_password = forms.CharField(widget = forms.PasswordInput)    
    
    class Meta:
        model = User
        
        fields = ('username','email','password','confirm_password')
        widgets = {'password':forms.PasswordInput()}
    
    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')              
        user = User.objects.create_user(username=username,email=email,password=password)
        return user.id      
    
    def clean(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if not username[0].isalpha():
            raise forms.ValidationError('Username Should start with Letter')
        if len(password)<7 or not any(pas.isdigit() for pas in password) or not any(pas.isalpha() for pas in password):          
                raise forms.ValidationError("password should have a leangth of 8 and contains alphanumeric values")
        if password!=confirm_password:
            raise forms.ValidationError('password not matching')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken')  
        if User.objects.filter(username=username).exists() :
            raise forms.ValidationError('Username exists')
            
        
        


        
              
