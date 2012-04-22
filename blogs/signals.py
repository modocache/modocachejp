from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context

from blogs.models import Blog, Tag, Post


@receiver(post_save, sender=User)
def create_blog_for_new_user(sender, instance, created, **kwargs):
    if created:
        b = Blog(user=instance)
        try:
            b.clean()
        except ValidationError:
            pass
        else:
            b.save()


@receiver(post_save, sender=Blog)
def create_tutorial_post_for_new_blog(sender, instance, created, **kwargs):
    if created:
        t = Tag.objects.get_or_create(blog=instance, name='Site Info')[0]

        post_template = get_template('blogs/rendered/post_sample_body.md')
        context = Context({})
        p = Post(
            blog=instance,
            title='Hello, World',
            body=post_template.render(context)
        )
        p.save()
        p.tags.add(t)


@receiver(post_save, sender=Blog)
def clear_cache_for_new_blog(sender, instance, created, **kwargs):
    cache.clear()


@receiver(post_save, sender=Post)
def clear_cache_for_new_post(sender, instance, created, **kwargs):
    cache.clear()
