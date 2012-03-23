from django.contrib import admin
from blogs.models import Blog, Tag, Post

admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Post)
