from tastypie.authentication import ApiKeyAuthentication, \
                                    BasicAuthentication, \
                                    MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource

from blogs.models import Blog, Tag, Post


class ProtectedResourceMixin(object):
    class Meta(object):
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()

class BlogResource(ModelResource, ProtectedResourceMixin):
    class Meta(object):
        queryset = Blog.objects.all()


class TagResource(ModelResource, ProtectedResourceMixin):
    class Meta(object):
        queryset = Tag.objects.all()


class PostResource(ModelResource, ProtectedResourceMixin):
    class Meta(object):
        # FIXME - Filter based on user permissions
        queryset = Post.objects.all()
