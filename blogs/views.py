from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, \
                                 DeleteView, ListView, DayArchiveView, \
                                 MonthArchiveView, YearArchiveView

from blogs.forms import PostForm
from blogs.models import Tag, Post


PAGINATE_BY = 3


class TagDetailView(DetailView):
    context_object_name = 'tag'
    model = Tag
    template_name = 'blogs/post_list.html'

    def get_object(self):
        return get_object_or_404(
            self.model.objects, slug=self.kwargs.get('tag_slug'))

    def get_context_data(self, **kwargs):
        tag = self.get_object()
        context = super(TagDetailView, self).get_context_data(**kwargs)
        posts = tag.posts.filter(is_public=True).order_by('-created_at')
        paginator = Paginator(posts, PAGINATE_BY)
        page = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['paginator'] = paginator
        context['page_obj'] = context['posts'] = page_obj
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


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        print dir(self)
        self.object = form.save(commit=False)
        self.object.blog = self.request.user.blog
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(UpdateView):
    context_object_name = 'post'
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('posts_list')


class PostListMixin(object):
    """
    A convenience class uses to provide common values
    to use in generic List- and ArchiveViews.
    """
    context_object_name = 'posts'
    model = Post
    queryset = Post.public.all()
    paginate_by = PAGINATE_BY
    date_field = 'created_at'
    month_format = '%m'
    make_object_list = True
    template_name = 'blogs/post_list.html'

    def get_queryset(self):
        """Order in descending order of date."""
        return super(PostListMixin, self).get_queryset().order_by(
            '-'+self.date_field)

class PostListView(PostListMixin, ListView):
    pass
class PostDayArchiveView(PostListMixin, DayArchiveView):
    pass
class PostMonthArchiveView(PostListMixin, MonthArchiveView):
    pass
class PostYearArchiveView(PostListMixin, YearArchiveView):
    pass
