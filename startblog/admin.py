from django.contrib import admin
from .models import Comments, Gallery,Blogs,Likes,Subscriber
# Register your models here.

admin.site.register(Gallery)
admin.site.register(Blogs)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Subscriber)