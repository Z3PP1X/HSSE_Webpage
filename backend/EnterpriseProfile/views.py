"""
Views for the Branch Network APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .branchNetwork.BranchNetwork import BranchNetwork


class BranchRecordViewSet(viewsets.ModelViewSet):
    """
    Endpoint for CRUD operations on the DFA Model.
    """

    queryset = BranchNetwork.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = ('CostCenter')

    def get_queryset(self):
        return self.queryset.filter(
            Active=True
        )

