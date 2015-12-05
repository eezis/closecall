from django.contrib.auth.models import User, Group
from incident.models import Incident
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')


class IncidentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Incident
        # fields = ('id', 'position', 'date', 'time')
        fields = ('id', 'date', 'time', 'latitude', 'longitude')