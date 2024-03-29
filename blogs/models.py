import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
import pytz

from blogs.utils import convert_markdown


def get_defaul_blog_tz():
    tzs = pytz.common_timezones
    if hasattr(settings, 'BLOGS_DEFAULT_TIME_ZONE'):
        return tzs.index(settings.BLOGS_DEFAULT_TIME_ZONE)
    else:
        return tzs.index(settings.TIME_ZONE)


class DatedModel(models.Model):
    """
    Abstract base class with created and updated
    time fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        default=datetime.datetime.utcnow(),
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        default=datetime.datetime.utcnow(),
        editable=False
    )
    timezone = models.IntegerField(
        choices=enumerate(pytz.common_timezones),
        default=get_defaul_blog_tz()
    )

    class Meta(object):
        abstract = True

    def _field_at_localtime(self, field):
        self_time = getattr(self, field)
        to_tz = pytz.timezone(pytz.common_timezones[int(self.timezone)])
        naive_time = self_time.replace(tzinfo=None)
        return self_time + to_tz.utcoffset(naive_time)

    @property
    def created_at_localtime(self):
        return self._field_at_localtime('created_at')

    @property
    def updated_at_localtime(self):
        return self._field_at_localtime('updated_at')


class Blog(DatedModel):
    """A blog, one of which exists for each user."""
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'

    def __unicode__(self):
        return '<Blog: {user}\'s blog>'.format(user=self.user.username)

    def clean(self):
        if Blog.objects.count() > 0:
            raise ValidationError('A blog already exists. Only one blog '
                                  'may exist per application.')


class Tag(DatedModel):
    """A tag used to organize posts."""
    blog = models.ForeignKey(Blog)
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=25, unique=True, blank=True)

    class Meta(object):
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        unique_together = (('blog', 'slug'),)

    def __unicode__(self):
        return '<Tag: {name} in {blog}>'.format(
            name=self.name, blog=self.blog)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('tags_detail', (), {'tag_slug': self.slug})


class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).\
            get_query_set().filter(is_public=True)


class Post(DatedModel):
    """A post made to the user blog."""
    blog = models.ForeignKey(Blog)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True)
    body = models.TextField()
    body_html = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)

    objects = models.Manager()
    public = PublicManager()

    class Meta(object):
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __unicode__(self):
        return '<Post: {slug}>'.format(slug=self.slug)

    def clean(self):
        # Ensure date and slug are unique together
        slug_date = datetime.datetime.utcnow()
        if self.created_at:
            slug_date = self.created_at

        duplicates = Post.objects.filter(
            created_at__year=slug_date.year,
            created_at__month=slug_date.month,
            created_at__day=slug_date.day,
            slug=slugify(self.title)
        )
        if self.pk:
            duplicates = duplicates.exclude(pk=self.pk)

        if duplicates:
            raise ValidationError('A post with an identical '
                                  'slug already exists for that date.')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.body_html = convert_markdown(self.body)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('posts_detail', (), {
            'year': self.created_at.year,
            'month': self.created_at.month,
            'day': self.created_at.day,
            'slug': self.slug,
        })


from blogs.signals import *
