from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, ArchiveIndexView, \
                                 DayArchiveView, MonthArchiveView, \
                                 YearArchiveView

from blogs.models import Tag, Post


class TagDetailView(DetailView):
    context_object_name = 'tag'
    model = Tag

    def get_object(self):
        return get_object_or_404(
            self.model.objects, slug=self.kwargs.get('tag_slug'))

    def get_context_data(self, **kwargs):
        tag = self.get_object()
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['posts'] = tag.posts.all()
        return context


class PostDetailView(DetailView):
    context_object_name = 'post'
    model = Post

    def get_object(self):
        return get_object_or_404(
            self.model.objects,
            created_at__year=self.kwargs.get('year'),
            created_at__month=self.kwargs.get('month'),
            created_at__day=self.kwargs.get('day'),
            slug=self.kwargs.get('slug')
        )


class PostListMixin(object):
    """
    A convenience class uses to provide common values
    to use in generic List- and ArchiveViews.
    """
    context_object_name = 'posts'
    model = Post
    paginate_by = 4
    date_field = 'created_at'
    month_format = '%m'
    make_object_list = True

    def get_queryset(self):
        """Order in descending order of date."""
        return super(PostListMixin, self).get_queryset().order_by(
            '-'+self.date_field)

class PostListView(PostListMixin, ListView):
    pass
class PostArchiveIndexView(PostListMixin, ArchiveIndexView):
    pass
class PostDayArchiveView(PostListMixin, DayArchiveView):
    pass
class PostMonthArchiveView(PostListMixin, MonthArchiveView):
    pass
class PostYearArchiveView(PostListMixin, YearArchiveView):
    pass
