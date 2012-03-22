from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context

from posts.models import Blog, Tag, Post


@receiver(post_save, sender=User)
def create_blog_for_new_user(sender, instance, created, **kwargs):
    if created:
        b = Blog(user=instance)
        b.save()


@receiver(post_save, sender=Blog)
def create_tutorial_post_for_new_blog(sender, instance, created, **kwargs):
    if created:
        t = Tag(blog=instance, name='Tutorial')
        t.save()

        post_template = get_template('posts/markdown/tutorial_post.md')
        context = Context({})
        p = Post(
            blog=instance,
            title='Hello, World',
            body=post_template.render(context)
        )
        p.save()
        p.tags.add(t)
