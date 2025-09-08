from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializers import CombinedEmergencyFormSerializer  # Import from serializers.py
from .models import Alarmplan, ContactPerson
from JsonSchemaForms.Factory.form_schema_factory import get_form_factory
from rest_framework.permissions import AllowAny

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
    
    @action(detail=False, methods=['get'])
    def form_schema(self, request):
        """Get combined form schema for emergency planning."""
        schema = CombinedEmergencyFormSerializer.get_form_schema()
        return Response(schema)
    
    def create(self, request):
        """Create an emergency plan with associated contacts."""
        # Implementation for creating combined Alarmplan + ContactPersons
        pass
    
    def update(self, request, pk=None):
        """Update an emergency plan with associated contacts."""
        # Implementation for updating combined data
        pass