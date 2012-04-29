import datetime

from django.contrib.auth.models import User, Permission
from django.core.exceptions import FieldError, ValidationError
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
import pytz

from blogs.utils import convert_markdown
from modocachejp.utils import get_function_name


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

    @classmethod
    def localtime(cls, utc_time, int_timezone):
        to_tz = pytz.timezone(pytz.common_timezones[int_timezone])
        naive_time = utc_time.replace(tzinfo=None)
        return utc_time + to_tz.utcoffset(naive_time)

    @classmethod
    def field_at_localtime(cls, obj, field):
        obj_time = getattr(obj, field)
        return DatedModel.localtime(obj_time, int(obj.timezone))

    @property
    def created_at_localtime(self):
        return DatedModel.field_at_localtime(self, 'created_at')

    @property
    def updated_at_localtime(self):
        return DatedModel.field_at_localtime(self, 'updated_at')


class PermissionModel(models.Model):
    """
    Abstract base class which allows models to give users
    permissions when saved.
    """
    class Meta(object):
        abstract = True

    def get_user(self):
        if hasattr(self, 'user'):
            return self.user
        else:
            raise FieldError(
                '{cls_name} must override {func_name} to return a '
                'User instance with associated permissions.'.format(
                    cls_name=self.__class__.__name__,
                    func_name=get_function_name(),
                )
            )

    def add_permissions(self, add=True, change=True, delete=True):
        user = self.get_user()
        for perm_action in ['add', 'change', 'delete']:

            if (add and perm_action == 'add') or \
               (change and perm_action == 'change') or \
               (delete and perm_action == 'delete'):

                codename = '{action}_{model}'.format(
                    action=perm_action,
                    model=self._meta.object_name.lower()
                )
                perm = Permission.objects.get_by_natural_key(
                    codename=codename,
                    app_label=self._meta.app_label,
                    model=self._meta.object_name.lower()
                )
                user.user_permissions.add(perm)

    def save(self, *args, **kwargs):
        super(PermissionModel, self).save(*args, **kwargs)
        self.add_permissions()


class Blog(DatedModel, PermissionModel):
    """A blog, one of which exists for each user."""
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'

    def __unicode__(self):
        return '<Blog: {user}\'s blog>'.format(user=self.user.username)

    def clean(self):
        if Blog.objects.count() > 0 and Blog.objects.all()[0] != self:
            raise ValidationError('A blog already exists. Only one blog '
                                  'may exist per application.')


class Tag(DatedModel, PermissionModel):
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

    def get_user(self):
        return self.blog.user

    @models.permalink
    def get_absolute_url(self):
        return ('tags_detail', (), {'tag_slug': self.slug})


class PublicManager(models.Manager):
    """Limits queries to public Posts."""
    def get_query_set(self):
        return super(PublicManager, self).\
            get_query_set().filter(is_public=True)


class Post(DatedModel, PermissionModel):
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

    def get_user(self):
        return self.blog.user

    def _absolute_url_for(self, url_name):
        return (url_name, (), {
            'year': self.created_at.year,
            'month': self.created_at.month,
            'day': self.created_at.day,
            'slug': self.slug,
        })

    @models.permalink
    def get_absolute_url(self):
        return self._absolute_url_for('posts_detail')

    @models.permalink
    def get_absolute_edit_url(self):
        return self._absolute_url_for('posts_update')

    @models.permalink
    def get_absolute_delete_url(self):
        return self._absolute_url_for('posts_delete')


from blogs.signals import *
