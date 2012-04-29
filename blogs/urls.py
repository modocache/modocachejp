from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from blogs.views import TagDetailView, PostListView, PostDetailView, \
                        PostUpdateView, PostDayArchiveView, \
                        PostMonthArchiveView, PostYearArchiveView, \
                        PostCreateView, PostDeleteView


urlpatterns = patterns('',
    url(
        regex=r'^tagged/(?P<tag_slug>[-\w]+)/$',
        view=TagDetailView.as_view(),
        name='tags_detail',
    ),
    url(
        regex=r'^$',
        view=PostListView.as_view(),
        name='posts_list',
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{1,2})/'
               '(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view=PostDetailView.as_view(),
        name='posts_detail',
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{1,2})/'
               '(?P<day>\d{1,2})/(?P<slug>[-\w]+)/update/$',
        view=PostUpdateView.as_view(),
        name='posts_update',
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{1,2})/'
               '(?P<day>\d{1,2})/(?P<slug>[-\w]+)/delete/$',
        view=PostDeleteView.as_view(),
        name='posts_delete',
    ),
    url(
        regex=r'^create/$',
        view=login_required(PostCreateView.as_view()),
        name='posts_create',
    ),
    url(
        regex=r'^(?P<year>\d{4})/$',
        view=PostYearArchiveView.as_view(),
        name='posts_archive_year',
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view=PostMonthArchiveView.as_view(),
        name='posts_archive_month',
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{1,2})/'
               '(?P<day>\d{1,2})/$',
        view=PostDayArchiveView.as_view(),
        name='posts_archive_day',
    ),
)
