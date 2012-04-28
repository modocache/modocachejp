from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, \
                                    BasicAuthentication, \
                                    MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.throttle  import BaseThrottle

from blogs.models import DatedModel, Blog, Tag, Post


class RestKitResourceMixin(object):
    def _get_object_class_name(self):
        return self._meta.object_class.__name__.split('.')[-1]

    def _get_data_key_name(self):
        """Return name of object class, pluralized."""
        return self._get_object_class_name().lower() + 's'

    def alter_list_data_to_serialize(self, request, data):
        data_key = self._get_data_key_name()
        data[data_key] = data['objects']
        del data['objects']
        return data

    def alter_deserialized_list_data(self, request, data):
        data_key = self._get_data_key_name()
        data['objects'] = data[data_key]
        del data[data_key]
        return data


class DatedModelResourceMixin(object):
    def _simple_time_string(self, dt):
        return str(dt).split('.')[0]

    def dehydrate(self, bundle):
        obj_created_at = bundle.data.get('created_at', None)
        obj_updated_at = bundle.data.get('updated_at', None)
        obj_timezone = bundle.data.get('timezone', None)

        if obj_timezone and obj_created_at and obj_updated_at:
            ca_local = DatedModel.localtime(obj_created_at, obj_timezone)
            ua_local = DatedModel.localtime(obj_updated_at, obj_timezone)

            ca_str = self._simple_time_string(ca_local)
            ua_str = self._simple_time_string(ua_local)

            bundle.data['created_at_localtime'] = ca_str
            bundle.data['updated_at_localtime'] = ua_str

        return bundle


class ProtectedResource(ModelResource):
    class Meta(object):
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()
        cache = SimpleCache()
        throttle = BaseThrottle(throttle_at=60, timeframe=60, expiration=60)


class BlogsModelResource(
    RestKitResourceMixin, DatedModelResourceMixin, ProtectedResource):
    pass


class BlogResource(BlogsModelResource):
    user = fields.ToOneField('modocachejp.api.UserResource', 'user', full=True)

    class Meta(object):
        queryset = Blog.objects.all()


class TagResource(BlogsModelResource):
    blog = fields.ForeignKey(BlogResource, 'blog', full=True)

    class Meta(object):
        queryset = Tag.objects.all()


class PostResource(BlogsModelResource):
    blog = fields.ForeignKey(BlogResource, 'blog', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)

    class Meta(object):
        # FIXME - Filter based on user permissions
        queryset = Post.objects.all()
