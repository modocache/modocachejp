from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_syncdb
from django.dispatch import receiver


@receiver(post_syncdb)
def configure_site_object(sender, created_models, **kwargs):
    if Site in created_models:
        try:
            current_site = Site.objects.get(id=settings.SITE_ID)
        except Site.DoesNotExist:
            current_site = Site(id=settings.SITE_ID)

        current_site.domain = settings.SITE_DOMAIN
        current_site.name = settings.SITE_NAME
        current_site.save()
