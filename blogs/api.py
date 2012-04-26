from tastypie.authentication import ApiKeyAuthentication, \
                                    BasicAuthentication, \
                                    MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.throttle  import BaseThrottle

from blogs.models import Blog, Tag, Post


class ProtectedResourceMixin(object):
    class Meta(object):
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()
        cache = SimpleCache()
        throttle = BaseThrottle(throttle_at=60, timeframe=60, expiration=60)


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
