from django.contrib.sites.models import Site

def site_details(request):
    return {
        'current_site': Site.objects.get_current(),
        'request': request,
    }
