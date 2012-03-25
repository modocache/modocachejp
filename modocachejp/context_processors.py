from django.contrib.sites.models import Site

def site_details(request):
    try:
        current_site = Site.objects.get_current()
    except Site.DoesNotExist:
        current_site = None
    return {
        'current_site': current_site,
        'request': request,
    }
