"""
Views for the Branch Network APIs.
"""

from rest_framework import viewsets, status, generics, filters
from rest_framework.response import Response


from .branchNetwork.BranchNetwork import BranchNetwork
from Core.management.commands import import_branches

from . import serializers

import json

import threading


class BranchRecordViewSet(viewsets.ModelViewSet):
    """
    Endpoint for CRUD operations on the DFA Model.
    """

    serializer_class = serializers.BranchUpdateSerializer
    queryset = BranchNetwork.objects.all()

    lookup_field = ('CostCenter')

    def get_queryset(self):
        return self.queryset.filter(
            Active=True
        )

    def update(self, request, *args, **kwargs):
        """Handles PUT requests without using the serializer"""

        try:
            data = json.loads(request.body)

            thread = threading.Thread(
                target=import_branches,
                args=('process_payload',),
                kwargs={'payload': json.dumps(data)}
            )
            thread.start()

            return Response({}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class CostCenterListView(generics.ListAPIView):
    """

    Endpoint for retrieving a list of cost centers.
    """

    queryset = BranchNetwork.objects.all()
    serializer_class = serializers.BranchUpdateSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
                    '^CostCenter',
                    '^BranchName',
                    'BranchName',
                     ]
