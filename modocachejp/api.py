from django.contrib.auth.models import User
from tastypie import fields

from blogs.api import ProtectedResource


class UserResource(ProtectedResource):
    blog = fields.ToOneField('blogs.api.BlogResource', 'blog')

    class Meta(object):
        queryset = User.objects.all()
        excludes = [
            'is_active',
            'is_staff',
            'is_superuser',
            'password'
        ]
