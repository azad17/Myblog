from django.urls import path
from .import views

app_name='startblog'

urlpatterns = [
    path('',views.home,name='home'),
    path('add_blog',views.add_blog,name='add_blog'),
]
