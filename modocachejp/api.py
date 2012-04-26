from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, \
                                    BasicAuthentication, \
                                    MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.throttle  import BaseThrottle

from blogs.api import BlogResource


class UserResource(ModelResource):
    blog = fields.ToOneField(BlogResource, 'blog')

    class Meta(object):
        queryset = User.objects.all()
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()
        cache = SimpleCache()
        throttle = BaseThrottle(throttle_at=60, timeframe=60, expiration=60)
        excludes = [
            'is_active',
            'is_staff',
            'is_superuser',
            'password'
        ]
