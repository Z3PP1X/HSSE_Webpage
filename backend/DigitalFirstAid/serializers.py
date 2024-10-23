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
            'sys_id', 'RequestedFor', 'IncidentDateTime',
            'TypeOfIncident', 'InjuryOccurence',
            'AccidentCause', 'PersonalProtectiveEquipment',
            'WorkContinuation',
        )
        read_only_fields = ('sys_id',)
