from django.forms import ModelForm, widgets
from .models import Blogs,Gallery

class BlogsForm(ModelForm):
    class Meta:
        model = Blogs
        fields = ('bloger','coverpic','title','content','personal')
        widgets = {'bloger':widgets.HiddenInput}


