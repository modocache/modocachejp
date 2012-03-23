from django.conf.urls import patterns, url

from posts.views import PostListView, PostDetailView


urlpatterns = patterns('',

    url(
        regex=r'^$',
        view=PostListView.as_view(),
        name='posts_list',
    ),

    url(
        regex=r'(?P<year>\d{4})/(?P<month>\d{1,2})/'
               '(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view=PostDetailView.as_view(),
        name='posts_detail',
    ),

)
