from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from posts.models import Post


class PostListView(ListView):
    context_object_name = 'posts'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
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

