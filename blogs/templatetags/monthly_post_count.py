from django import template

from blogs.models import Post


register = template.Library()


@register.inclusion_tag('blogs/templatetags/monthly_post_count.html')
def monthly_post_count():
    ret = {}
    dates = Post.objects.dates('created_at', 'month', order='DESC')
    for date in dates:
        ret[date.date] = Post.objects.filter(
            created_at__year=date.year,
            created_at__month=date.month
        ).count()

    return {'monthly_post_count':ret.items()}
