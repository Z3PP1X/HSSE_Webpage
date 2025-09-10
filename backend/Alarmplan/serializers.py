from rest_framework import serializers
from .models import Alarmplan, ContactPerson
from JsonSchemaForms.Factory.form_schema_factory import get_form_factory
from .config import ALARMPLAN_FORM_CONFIG


class CombinedEmergencyFormSerializer(serializers.Serializer):
    """Serializer for combined emergency planning form using multiple models."""

    @staticmethod
    def get_form_schema():
        """Generate form schema combining Alarmplan and ContactPerson models."""
        factory = get_form_factory('multi')
        creator = factory.create_form_creator(
            models={
                'Alarmplan': Alarmplan,
                'ContactPerson': ContactPerson
            },
            form_id="alarmplan_form",
            form_title="Emergency Alarm Plan"
        )
        # Use the imported config instead of inline config
        creator.configure_from_dict(ALARMPLAN_FORM_CONFIG)
        return creator.build()
