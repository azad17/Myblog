from django.urls import path
from .import views
app_name = 'blogapp'
urlpatterns = [
    path("home",views.home,name='home'),
    path("",views.register,name='register'),
    path("login/",views.login,name='login'),
    path("userlist/",views.UserList.as_view(),name='userlist'),
    path("userdetails/<int:pk>/",views.UserDetails.as_view(),name='userdetails'),
    path('userupdate/<int:pk>/',views.UserUpdate.as_view(),name='userupdate'),
    path('userdelete/<int:pk>/',views.UserDelete.as_view(),name='userdelete'),
    path("logout",views.user_logout,name='logout'),
]