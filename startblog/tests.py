from logging import log
from django import setup
from django.contrib.auth import login
from django.contrib.auth.forms import UsernameField
from django.db.models.query_utils import RegisterLookupMixin
from django.http import request, response
from django.test import TestCase, Client,  client
from django.urls import reverse
from django.contrib.auth.models import User
from startblog.models import Blogs, Likes, Comments, Subscriber, Gallery
from .views import *
from .models import Blogs, Gallery, Likes, Subscriber, Comments
from django.core.files.uploadedfile import SimpleUploadedFile


class UrlTest(TestCase) :


    def setUp(self):
        self.factory = client.RequestFactory()
        request.session = {}
    

    def test_home(self): 
        request = self.factory.get('/startblog/')
        request.user = User.objects.create_user('mammu', 'mammu@gmail.com', 'password')
        response = home(request)
        self.assertEquals(response.status_code,200) 
    

    def test_all_blog(self):
        user = User.objects.create_user('pappu','pappu@gmail.com', 'password')
        self.blog = Blogs.objects.create(bloger=user,title='newtitle', content='testalblog', personal=False, coverpic='paris.jpg')  
        response = self.client.get('/startblog/all_blog')
        self.assertEquals(response.status_code,200)
        

    def test_user_profile(self):
        request = self.factory.get('/startblog/user_profile')
        request.user = User.objects.create_user('mammu', 'mammu@gmail.com', 'password')
        response = user_profile(request)
        self.assertEquals(response.status_code,200) 
    

    def test_bloger_profile_get(self):
        request = self.factory.get('/startblog/bloger_profile/')
        request.user = User.objects.create_user('mammu', 'mammu@gmail.com', 'password')
        args = request.user.pk
        response = bloger_profile(request,args)
        self.assertEquals(response.status_code,200)
    

    def test_bloger_profile_post(self):
        user = User.objects.create_user('mammu', 'mammu@gmail.com', 'password')
        data = {'sub':'subscriber@gmail.com'}
        response = self.client.post('/startblog/bloger_profile/{}/'.format(user.id), data=data)
        self.assertEquals(response.status_code,302)
   

    def test_add_blog(self):
        self.user = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        self.client.login(username='user1', password='password')
        self.pic = SimpleUploadedFile(name='kerala.jpg', content=open('/home/azad/mj/Myblog/media/pics/kerala.jpeg', 'rb').read(), content_type='image/jpeg')
        image = SimpleUploadedFile("dog.jpg", b"file_content", content_type="image/jpg")  
        self.subscriber = Subscriber.objects.create(user=self.user, sub='subscriber@gmail.com.com')
        self.data =  {'title': 'mtitle', 'content': 'conte', 'personal':False,'coverpic': self.pic, 'images':image}
        response = self.client.post(reverse('startblog:add_blog'), self.data,follow=True)
    

    def test_blog_update(self):
        self.user = User.objects.create_user('man', 'man@gmail.com', 'password')
        self.client.login(username='man', password='password') 
        image = SimpleUploadedFile("dog.jpg", b"file_content", content_type="image/jpg")
        self.blog = Blogs.objects.create(bloger=self.user,title='newtitle', content='cont', personal=False,coverpic='paris.jpg') 
        self.data = {'bloger': self.blog.bloger,'title': 'mtitle','content': 'conte', 'personal': False, 'coverpic': 'paris.jpg', 'images': image}
        response = self.client.post(reverse('startblog:blog_update', kwargs={'pk':self.blog.pk}), self.data,follow=True)
        self.assertEqual(response.request.get("PATH_INFO"), '/startblog/user_profile')


    def test_image_delete(self):
        self.user = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        self.client.login(username='user1', password = 'password')
        self.blog = Blogs.objects.create(bloger=self.user, title='newtitle', content='cont', personal=False, coverpic='paris.jpg')
        self.pic = SimpleUploadedFile(name='kerala.jpg', content=open('/home/azad/mj/Myblog/media/pics/kerala.jpeg', 'rb').read(), content_type='image/jpeg')
        self.pics = Gallery.objects.create(blog = self.blog,photo = self.pic)
        response = self.client.post(reverse('startblog:image_delete', kwargs={'pk':self.pics.pk}), follow=True)
        self.assertEqual(response.request.get("PATH_INFO"), '/startblog/user_profile')
    

    def test_add_like(self):
        self.user = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        self.blog = Blogs.objects.create(bloger=self.user,title='newtitle', content='cont', personal=False, coverpic='paris.jpg')
        self.client.login(username='user1', password='password')
        self.data= {'like': 'like'}
        response = self.client.post(reverse('startblog:add_like',kwargs = {'pk': self.blog.id}), self.data,follow=True)
        self.assertEqual(Likes.objects.all().count(), 1)
        self.data= {'like':'unlike'}
        response = self.client.post(reverse('startblog:add_like', kwargs = {'pk': self.blog.id}), self.data,follow=True)
        self.assertEqual(Likes.objects.all().count(),0)
    
    def test_add_comment(self):
        self.user = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        self.client.login(username='user1', password='password') 
        self.blog = Blogs.objects.create(bloger=self.user,title='newtitle',content='cont',personal=False,coverpic='paris.jpg')
        self.data = {'comment':'mycomment'}
        response = self.client.post(reverse('startblog:add_comment',kwargs={'pk': self.blog.id}), self.data,follow=True)
        self.assertEqual(Comments.objects.all().count(),1)


    def test_view_comments(self):
        self.user = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        self.blog = Blogs.objects.create(bloger=self.user, title='newtitle',content='cont', personal=False, coverpic='paris.jpg')
        Comments.objects.create(post=self.blog,cmnt='good',comented_by = self.user)
        response = self.client.get(reverse('startblog:view_comments', kwargs={'pk': self.blog.id}), follow=True)
        self.assertEquals(response.status_code, 200)


    def test_comment_delete(self):
        self.user = User.objects.create_user('user1', 'user1@gmail.com', 'password')
        self.blog = Blogs.objects.create(bloger=self.user,title='newtitle', content='cont', personal=False, coverpic='paris.jpg')
        self.comment = Comments.objects.create(post=self.blog, cmnt='good', comented_by = self.user)
        self.assertEqual(Comments.objects.all().count(), 1)
        response = self.client.post(reverse('startblog:comment_delete', kwargs={'pk': self.comment.id}), follow=True)
        self.assertEqual(Comments.objects.all().count(), 0)
      

    def test_password_reset_request(self):
        self.user = User.objects.create_user('man', 'dummy@gmail.com', 'qwerty1234')
        self.data = {'email':'dummy@gmail.com@gmail.com'}
        response = self.client.post(reverse('startblog:password_reset'), self.data, follow=True)