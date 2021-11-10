
from django import forms
from django.forms import ModelForm, fields, widgets
from .models import Blogs,Gallery

class BlogsForm(ModelForm):
    
    class Meta:
        model = Blogs
        fields = ('bloger','coverpic','title','content','personal')
        widgets = {'bloger':widgets.HiddenInput,'content':widgets.Textarea}
 
class GalleryForm(ModelForm):

    class Meta:
        model = Gallery
        fields = ('photo',) 
             
       

                
    
