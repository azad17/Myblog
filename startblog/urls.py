from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name='startblog'
urlpatterns = [
    path('',views.home,name='home'),
    path('add_blog',views.add_blog,name='add_blog'),
    path('all_blog',views.all_blog,name='all_blog'),
    path('blog_update/<int:pk>/',views.blog_update,name='blog_update'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('pass_change',auth_views.PasswordChangeView.as_view(template_name='startblog/pass-change.html'),name='pass_change'),
    path('image_delete/<int:pk>/',views.image_delete,name='image_delete'),
    path('password_reset', views.password_reset_request, name="password_reset"),
    path('add_like/<int:pk>/',views.add_like,name='add_like'),
    
]
 