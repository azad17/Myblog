from django import setup
from django.db.models.expressions import F
from django.http import response
from django.test import TestCase, client
from .views import *
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
# Create your tests here.

class ViewTest(TestCase):


    def setUp(self):
        user1 = User(username='mamo', email='mam0@gmail.com')
        user1_pass = 'qwerty1234'
        user1.is_active = True
        user1.save()
        user1.set_password(user1_pass)
        self.user1_pass = user1_pass
        self.user1 = user1
        self.factory = client.RequestFactory()


    def test_home(self):
        self.user =  User.objects.create_user('jojo', 'jojo@gmail.com', 'qwerty1234') 
        self.user.is_admin = True
        self.client.login(username='jojo', password="qwerty1234")
        response = self.client.get('/blogapp/home')
        self.assertEquals(response.status_code, 200)
          
    
    def test_login(self):
        User.objects.create_user('jojo', 'jojo@gmail.com', 'password')
        self.client.login(username='jojo', password='password')
        response = self.client.get('/blogapp/user_login/')
        self.assertEquals(response.status_code, 200)
      
    
    def test_login_post(self):   
        User.objects.create_user('jojo', 'jojo@gmail.com', 'password') 
        data = {'username':'jojo', 'password': 'password'}
        response = self.client.post(reverse('blogapp:user_login'), data,follow=True) 
        redirect_path = response.request.get("PATH_INFO") 
        self.assertEqual(redirect_path, '/startblog/')
    
    
    def test_register(self):
        response = self.client.get('/blogapp/')
        self.assertEqual(response.status_code, 200)
        data = {'username': 'jojo', 'email': 'jojo@gmail.com', 'password': 'qwerty1234', 'confirm_password': 'qwerty1234'}
        response = self.client.post(reverse('blogapp:register'), data, follow=True)
        self.assertEqual(response.request.get('PATH_INFO'), '/blogapp/user_login/')
  
    
    def test_user_logout(self):
        User.objects.create_user('jojo', 'jojo@gmail.com', 'qwerty1234') 
        self.client.login(username='jojo', password="qwerty1234")
        response = self.client.get(reverse('blogapp:logout'), follow=True)
        self.assertEqual(response.request.get('PATH_INFO'), '/blogapp/user_login/')
        
    
    def test_user_list(self):
        self.user =  User.objects.create_user('jojo', 'jojo@gmail.com', 'qwerty1234') 
        self.user.is_admin = True
        self.client.login(username='jojo', password="qwerty1234")
        response = self.client.get(reverse('blogapp:userlist'), follow=True)
        self.assertEqual(response.status_code, 200)

    
    def test_user_details(self):
        self.user =  User.objects.create_user('jojo', 'jojo@gmail.com', 'qwerty1234') 
        self.user.is_admin = True
        self.client.login(username='jojo', password="qwerty1234")
        response = self.client.get(reverse('blogapp:userdetails', kwargs = {'pk': self.user.id}), follow=True)
        self.assertEqual(response.status_code, 200)
       
    
    def test_user_update(self):
        self.user = User.objects.create_user('joji', 'joji@gmail.com', 'qwerty1234') 
        response = self.client.post(reverse('blogapp:userupdate', kwargs = {'pk': self.user.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        
    
    def test_admin_update(self):
        self.user = User.objects.create_user('joji', 'joji@gmail.com', 'qwerty1234') 
        self.user.is_admin = True
        self.client.login(username='joji', password='qwerty1234')
        self.data = {'username': 'joj'}
        response = self.client.post(reverse('blogapp:adminupdate', kwargs = {'pk': self.user.id}), self.data, follow=True)
        self.assertEqual(response.request.get('PATH_INFO'), '/blogapp/home')

    
    def test_user_delete(self):
        self.user = User.objects.create_user('man', 'man@gmail.com', 'qwerty1234')
        response = self.client.post(reverse('blogapp:userdelete', kwargs = {'pk': self.user.id}), follow=True)
        self.assertEqual(response.request.get('PATH_INFO'), '/blogapp/userlist/')

    
    def test_admin_invites(self):
        self.user = User.objects.create_user('man', 'man@gmail.com', 'qwerty1234')
        self.client.login(username='man', password="qwerty1234")
        self.user.is_admin = False
        response = self.client.get(reverse('blogapp:admin_invites', kwargs = {'pk': self.user.id}), follow=True)
        self.assertEqual(response.request.get('PATH_INFO'), '/blogapp/userlist/')
        
        
    


        
    

        


    
    

       
        
 
        


