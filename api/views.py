from incident.models import Incident
from rest_framework import viewsets
from serializers import IncidentSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that provides limited access to incident data
    """

    http_method_names = ['get', 'head']

    # NOTE, must use 'queryset' as the variable here
    # queryset = Incident.objects.all().values('id', 'position', 'date', 'time').order_by('-date')
    queryset = Incident.objects.all().values('id','date','time', 'latitude', 'longitude')
    serializer_class = IncidentSerializer