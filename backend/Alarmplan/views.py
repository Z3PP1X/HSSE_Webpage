from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializers import CombinedEmergencyFormSerializer
from .models import Alarmplan, ContactPerson
from JsonSchemaForms.Factory.form_schema_factory import get_form_factory
from rest_framework.permissions import AllowAny
from rest_framework import serializers

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

class CombinedEmergencyFormSerializer(serializers.Serializer):
    """Serializer for combined emergency planning form using multiple models."""
    
    @staticmethod
    def get_form_schema():
        """Generate form schema combining Alarmplan and ContactPerson models."""
        factory = get_form_factory('multi')
        creator = factory.create_form_creator(
            models={
                'alarmplan': Alarmplan,
                'contact': ContactPerson
            },
            form_id="alarmplan_form",
            form_title="Emergency Alarm Plan"
        )
        
        config = {
            'categories': [
                {
                    'key': 'plan_setup',
                    'title': 'Plan Configuration',
                    'fields': [
                        {'model': 'Alarmplan', 'field': 'Active'},
                        {
                            'model': 'Alarmplan', 
                            'field': 'RelatedBranch',
                            'ajax': {
                                'endpoint': '/api/branchnetwork/costcenters/',
                                'method': 'GET',
                                'events': ['input', 'focus'],
                                'debounce': 300,
                                'field_type': 'ajax_select',
                                'search_field': 'CostCenter',
                                'display_field': 'BranchName',
                                'value_field': 'sys_id'
                            }
                        }
                    ]
                },
                {
                    'key': 'emergency_contacts',
                    'title': 'Emergency Contact Persons',
                    'fields': [
                        {'model': 'ContactPerson', 'field': 'ContactPersonName'},
                        {'model': 'ContactPerson', 'field': 'ContactPersonEmail'},
                        {'model': 'ContactPerson', 'field': 'ContactPersonPhoneNumber'},
                        {'model': 'ContactPerson', 'field': 'ContactType'}
                    ]
                }
            ]
        }
        
        creator.configure_from_dict(config)
        return creator.build()

# In Factory/json_form_creator.py - MultiModelFormCreator class
def configure_from_dict(self, config: dict):
    """Configure the form schema from a dictionary with dynamic AJAX support."""
    
    # Apply AJAX configs
    if 'ajax_configs' in config:
        for key, cfg in config['ajax_configs'].items():
            self.add_ajax_config(
                key, 
                cfg['endpoint'], 
                method=cfg.get('method', 'GET'),
                events=cfg.get('events'),
                debounce=cfg.get('debounce', 300)
            )
    
    # Handle categories with model-specific field mapping
    if 'categories' in config:
        for cat in config['categories']:
            field_configs = []
            
            for field_spec in cat.get('fields', []):
                if isinstance(field_spec, str):
                    # Simple field reference
                    if field_spec in self.all_model_fields:
                        field_info = self.all_model_fields[field_spec].copy()
                        field_configs.append(field_info)
                        
                elif isinstance(field_spec, dict):
                    # Complex field specification with model info
                    model_name = field_spec.get('model')
                    field_name = field_spec.get('field')
                    
                    if model_name and field_name:
                        prefixed_name = f"{model_name.lower()}_{field_name}"
                        if prefixed_name in self.all_model_fields:
                            field_info = self.all_model_fields[prefixed_name].copy()
                            
                            # Apply field-specific overrides
                            if 'overrides' in field_spec:
                                field_info.update(field_spec['overrides'])
                            
                            # Handle dynamic AJAX configuration
                            if 'ajax' in field_spec:
                                ajax_config = field_spec['ajax']
                                
                                # Generate unique AJAX config key
                                ajax_key = f"{field_name}_ajax_{cat['key']}"
                                
                                # Add the AJAX config to shared configs
                                self.add_ajax_config(
                                    ajax_key,
                                    ajax_config['endpoint'],
                                    method=ajax_config.get('method', 'GET'),
                                    events=ajax_config.get('events', ['change']),
                                    debounce=ajax_config.get('debounce', 300)
                                )
                                
                                # Update field to reference the AJAX config
                                field_info.update({
                                    'field_type': ajax_config.get('field_type', 'ajax_select'),
                                    'ajax_config': ajax_key,
                                    'search_field': ajax_config.get('search_field'),
                                    'display_field': ajax_config.get('display_field'),
                                    'value_field': ajax_config.get('value_field', 'id')
                                })
                            
                            field_configs.append(field_info)
            
            self.add_category(cat['key'], cat['title'], field_configs)
    
    return self