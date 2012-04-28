from django.forms import ModelForm

from blogs.models import Post


class PostForm(ModelForm):
    class Meta(object):
        model = Post
        fields = ('title', 'body', 'tags', 'timezone', 'is_public')
