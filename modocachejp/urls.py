from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from tastypie.api import Api

from blogs.api import BlogResource, TagResource, PostResource
from modocachejp.api import UserResource


admin.autodiscover()


api_v1 = Api(api_name='v1')
api_v1.register(UserResource())
api_v1.register(BlogResource())
api_v1.register(TagResource())
api_v1.register(PostResource())


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogs.urls')),
    url(r'^api/', include(api_v1.urls)),
    url(
        regex=r'^$',
        view=RedirectView.as_view(url='/blog/'),
        name='site_index',
    ),
)
