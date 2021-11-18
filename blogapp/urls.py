from django.urls import path
from .import views
app_name = 'blogapp'
urlpatterns = [
    path("home",views.home,name='home'),
    path("",views.register,name='register'),
    path("user_login/",views.user_login,name='user_login'),
    path("userlist/",views.UserList.as_view(),name='userlist'),
    path("userdetails/<int:pk>/",views.UserDetails.as_view(),name='userdetails'),
    path('userupdate/<int:pk>/',views.UserUpdate.as_view(),name='userupdate'),
    path('userdelete/<int:pk>/',views.UserDelete.as_view(),name='userdelete'),
    path("logout",views.user_logout,name='logout'),
    path('admin_invites/<int:pk>/',views.admin_invites,name='admin_invites'),
    path('adminupdate/<int:pk>/',views.AdminUpdate.as_view(),name='adminupdate'),
   
    
]