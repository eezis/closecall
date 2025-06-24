from django.conf import settings

def google_maps_api_key(request):
    """
    Context processor to make Google Maps API key available to all templates
    """
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }