"""
Serializers for the digital first aid book apis.
"""

from rest_framework import serializers

from .hsseModules.FirstAidRecord import FirstAidRecord

from JsonSchemaForms.model_schema_builder import ModelFormSchemaBuilder


class FirstAidRecordSerializer(serializers.ModelSerializer):
    """Serializer for the first aid record object."""

    class Meta:
        model = FirstAidRecord
        fields = (
            'RequestedFor', 'IncidentDateTime',
            'TypeOfIncident', 'InjuryOccurence',
            'AccidentCause', 'PersonalProtectiveEquipment',
            'WorkContinuation', 'AccidentDescription',
            'AccidentWitness', 'FirstAidMeasures',
        )


class FirstAidRecordMetadataSerializer(serializers.BaseSerializer):
    """Serializer for the Models Metadata"""

    def get_model_metadata(model, meta_whitelist=[]):
        # Create a new ModelFormSchemaBuilder instance
        builder = ModelFormSchemaBuilder(
            model_class=model,
            form_id="first_aid_record_form",
            form_title="First Aid Record Form"
        )
        
        # Configure with dummy categories (to be replaced later)
        config = {
            'categories': [
                {
                    'key': 'incident_details',
                    'title': 'Incident Details',
                    'fields': ['RequestedFor', 'IncidentDateTime', 'TypeOfIncident', 'IncidentLocation']
                },
                {
                    'key': 'injury_information',
                    'title': 'Injury Information',
                    'fields': ['InjuryOccurence', 'AccidentCause', 'AccidentDescription']
                },
                {
                    'key': 'additional_info',
                    'title': 'Additional Information',
                    'fields': ['PersonalProtectiveEquipment', 'WorkContinuation', 
                               'AccidentWitness', 'FirstAidMeasures']
                }
            ]
        }
        
        # Configure builder from the config dictionary
        builder.configure_from_dict(config)
        
        # Return the built schema
        return builder.build()
