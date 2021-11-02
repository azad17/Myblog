from django.shortcuts import redirect, render
from startblog.models import Blogs
from .forms import  BlogsForm
from django.db.models import Q

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('blogapp:login')
    blog = Blogs.objects.filter(Q(personal=False)|Q(bloger=request.user))
    context = {'blog':blog}
    return render (request,'startblog/bloghome.html',context)
    
def add_blog(request):
    if not request.user.is_authenticated:
        return redirect('blogapp:login')
    form = BlogsForm()
    initial_dict ={'bloger':request.user}
    form = BlogsForm(request.POST or None ,initial=initial_dict)
    if request.method=='POST':      
        form = BlogsForm(request.POST,request.FILES,initial=initial_dict)
        if form.is_valid():
            form.save();
            return redirect('startblog:home')
    context = {}
    context['form']=form
    return render (request,'startblog/add-blog.html',context)
