
from django import forms
from django.forms import ModelForm, fields, widgets
from .models import Blogs,Gallery

class BlogsForm(ModelForm):
    
    class Meta:
        model = Blogs
        fields = ('bloger','coverpic','title','content','personal')
    '''making bloger field read only'''    
    def __init__(self, *args, **kwargs):
        super(BlogsForm, self).__init__(*args, **kwargs)
        self.fields['bloger'].disabled = True    
 
class GalleryForm(ModelForm):

    class Meta:
        model = Gallery
        fields = ('photo',) 
             
       

                
    
