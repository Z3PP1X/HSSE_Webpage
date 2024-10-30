""""
Views for the First Aid Book APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response

from .hsseModules.FirstAidRecord import FirstAidRecord
from . import serializers
from drf_spectacular.utils import extend_schema


class FirstAidRecordViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe APIs.
    """
    serializer_class = serializers.FirstAidRecordSerializer
    queryset = FirstAidRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = ('sys_id')

    def get_queryset(self):
        return self.queryset.filter(
            RequestedFor=self.request.user).order_by('-created_on')

