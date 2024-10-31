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




class FirstAidRecordViewSet(viewsets.ModelViewSet):
    """
    Endpoint for CRUD operations on the DFA Model.
    """
    serializer_class = serializers.FirstAidRecordSerializer
    queryset = FirstAidRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = ('sys_id')

    def get_queryset(self):
        return self.queryset.filter(
            RequestedFor=self.request.user).order_by('-created_on')

class MetaRecordView(APIView):
    """Endpoint for generating dynamic forms in the frontend"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return the metadata for the First Aid Record"""