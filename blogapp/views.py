from django.shortcuts import render,redirect

from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from .forms import UserForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
# Create your views here.

def home(request):
    return render(request,'blogapp/home.html')

def register(request):
    form = UserForm()
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogapp:login')       
    return render(request,'blogapp/register.html',{'form':form})

def login(request):
    if request.method=='POST':       
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            print(user)           
            return redirect('blogapp:home')
        else:
            messages.info(request,'Username/Password is Incorrect')
            redirect('blogapp:login')
    return render(request,'blogapp/login.html')  

def user_logout(request):
    logout(request)
    return redirect('blogapp:login')

class  UserList(ListView):
    model = User
    template_name = 'blogapp/userlist.html'
    context_object_name = 'user'

class  UserDetails(DetailView):    
    model = User
    template_name = 'blogapp/userdetails.html'
    context_object_name = 'user'

class UserUpdate(UpdateView):
    model = User
    fields = ('username','email','is_superuser')
    template_name = 'blogapp/userupdate.html'    
    def get_success_url(self):
        return reverse_lazy('blogapp:userdetails',kwargs = {'pk':self.object.id})

class UserDelete(DeleteView):
    model = User
    template_name  = 'blogapp/userdelete.html'
    context_object_name='user'
    success_url = reverse_lazy('blogapp:userlist')
            