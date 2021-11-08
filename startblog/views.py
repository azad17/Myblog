from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from startblog.models import Blogs, Gallery,Likes
from .forms import  BlogsForm, GalleryForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Exists,OuterRef
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('blogapp:login')
    blog = Blogs.objects.annotate (is_liked = Exists(Likes.objects.filter(liked_user=request.user,like_status=True,post_id=OuterRef('pk')))).all()
    context = {'blog':blog}
    return render (request,'startblog/bloghome.html',context)

def all_blog(request):
    blog = Blogs.objects.all()
    context = {'blog':blog}
    return render(request,'startblog/all-blog.html',context)   

def add_blog(request):
    if not request.user.is_authenticated:
        return redirect('blogapp:login')
    form = BlogsForm()   
    initial_dict ={'bloger':request.user}
    form = BlogsForm(request.POST or None ,initial=initial_dict)
    if request.method=='POST':      
        form = BlogsForm(request.POST,request.FILES,initial=initial_dict)       
        if form.is_valid():
            obj = form.save();
            obj = Blogs.objects.get(pk=obj.id)         
            images = request.FILES.getlist('images')
            for img in  images:
                Gallery.objects.create(blog =obj,photo=img)
            return redirect('startblog:home')
    context = {}
    context['form'] = form
    return render (request,'startblog/add-blog.html',context)

def blog_update(request,pk):
    blog  = Blogs.objects.get(id=pk)
    form = BlogsForm(instance=blog)
    if request.method=='POST':
        form = BlogsForm(request.POST or None, request.FILES, instance=blog)
        if form.is_valid():
            form.save() 
            print(blog)
            ob = Gallery.objects.filter(blog__title = blog)
            images = request.FILES.getlist('images')
            if images:
                for img in  images:
                    Gallery.objects.create(blog =blog,photo=img)
                return redirect('startblog:user_profile')          
            return redirect('startblog:user_profile')
    return render(request,'startblog/blog-update.html',{'form':form,})
    
def user_profile(request):
    blog = Blogs.objects.filter(bloger__username = request.user)
    photos = Gallery.objects.all()
    return render(request,'startblog/user-profile.html',{'blog':blog,'photos':photos})    
    
def image_delete(request,pk):
    if request.method == 'POST':
        pics = Gallery.objects.filter(pk=pk)
        for ob in pics:
            ob.delete()
            return redirect('startblog:user_profile')
    return render(request,'startblog/image-delete.html')    
   
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "passwords/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admim@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="passwords/password_reset.html", context={"password_reset_form":password_reset_form})

def add_like(request,pk):
    blog = Blogs.objects.get(pk=pk)  
    if request.method =='POST':
        if request.POST.get('like')=='like':
            like =Likes.objects.filter(post=blog,like_status=False,liked_user=request.user)   
            if like:
                like.update(like_status = True)
            else:
                like = Likes.objects.create(post=blog,like_status=True,liked_user=request.user)
                return redirect('startblog:home')
        if request.POST.get('like')=='unlike':
            post = Likes.objects.get(post=blog,liked_user=request.user)
            print(post)
            post.like_status = False
            post.save();
    return redirect('startblog:home')             