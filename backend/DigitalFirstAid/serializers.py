"""
Serializers for the digital first aid book apis.
"""

from rest_framework import serializers

from .hsseModules.FirstAidRecord import FirstAidRecord


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
        field_names = model._meta.fields
        return_data = {}
        super_attributes = ("id", "sys_id", "created_by",
                            "updated_by", "updated_on",
                            "created_on", "Active")

        for field in field_names:
            if field.name in super_attributes:
                continue

            field_name = field.name
            field_meta = field.__dict__
            return_meta = {}
            return_meta['key'] = field.name

            for meta_name in field_meta:
                if meta_name in meta_whitelist:
                    return_meta[meta_name] = field_meta[meta_name]
                    return_meta['field_type'] = field.get_internal_type()

                if field.choices:
                    return_meta['choices'] = [
                        {'value': choice[0], 'display_name': choice[1]}
                        for choice in field.choices]

            return_data[field_name] = return_meta

        return return_data
