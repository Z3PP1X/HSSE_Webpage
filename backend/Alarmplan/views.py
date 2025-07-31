from django.shortcuts import render

from . import serializers

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Alarmplan, ContactPerson

class AlarmplanViewSet(viewsets.ModelViewSet):
    """
    Endpoint for CRUD operations on the Alarmplan Model.
    """
    serializer_class = serializers.AlarmplanSerializer
    queryset = Alarmplan.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = ('RelatedBranch')

class ContactPersonViewSet(viewsets.ModelViewSet):
    """
    Endpoint for CRUD operations on the Contact Person Model.
    """

    serializer_class = serializers.ContactPersonSerializer
    queryset = ContactPerson.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = ('')
