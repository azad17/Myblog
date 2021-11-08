from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blogs(models.Model):
    bloger = models.ForeignKey(User,on_delete=models.CASCADE)
    coverpic = models.ImageField(upload_to='pics')
    title = models.CharField(unique=True,max_length=100)
    content = models.CharField(max_length=1000)
    personal = models.BooleanField()
    def __str__(self):
        return str(self.title)

class Likes(models.Model):
    post = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    like_status = models.BooleanField(default=False)
    liked_user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.like_status)

class Gallery(models.Model):
    blog = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='galery')  
    def __str__(self):
        return str(self.blog)      

