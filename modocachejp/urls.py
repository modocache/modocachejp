from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogs.urls')),
    url(
        regex=r'^$',
        view=RedirectView.as_view(url='/blog/'),
        name='site_index',
    ),
)

