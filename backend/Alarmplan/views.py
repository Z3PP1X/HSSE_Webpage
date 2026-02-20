from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets
from .serializers import CombinedEmergencyFormSerializer  # Import from serializers.py
from .models import Alarmplan
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class AlarmplanViewSet(viewsets.ModelViewSet):
    """ViewSet for Alarmplan operations - uses combined form approach."""
    queryset = Alarmplan.objects.all()
    serializer_class = CombinedEmergencyFormSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def form_schema(self, request):
        """Get combined form schema for Alarmplan creation/editing."""
        schema = CombinedEmergencyFormSerializer.get_form_schema()
        return Response(schema)


class EmergencyPlanningViewSet(viewsets.ViewSet):
    """ViewSet for emergency planning operations using combined models."""

    @extend_schema(
            responses={200: dict},
            description='Get combined form schema for emergency planning.'
    )
    @action(
        detail=False,
        methods=['get'])
    def form_schema(self, request):
        """Get combined form schema for emergency planning."""
        schema = CombinedEmergencyFormSerializer.get_form_schema()
        return Response(schema)

    @extend_schema(
            request=CombinedEmergencyFormSerializer,
            responses={201: CombinedEmergencyFormSerializer},
            description='Create an emergency plan with associated contacts.'
    )
    def create(self, request):
        """Create an emergency plan with associated contacts."""
        # Implementation for creating combined Alarmplan + ContactPersons
        pass

    @extend_schema(
            request=CombinedEmergencyFormSerializer,
            responses={200: CombinedEmergencyFormSerializer},
            parameters=[
                OpenApiParameter(
                    name='id',
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.PATH
                )
            ],
            description='Update an emergency plan with associated contacts.'
    )
    def update(self, request, pk=None):
        """Update an emergency plan with associated contacts."""
        # Implementation for updating combined data
        pass
