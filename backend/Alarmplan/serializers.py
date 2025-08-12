from rest_framework import serializers
from .models import Alarmplan, ContactPerson
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork
from JsonSchemaForms.Factory.form_schema_factory import get_form_factory

class AlarmplanSerializer(serializers.ModelSerializer):
    RelatedBranch = serializers.SlugRelatedField(
            slug_field='CostCenter',
            queryset=BranchNetwork.objects.all()
        )
    class Meta:
        model = Alarmplan
        fields = '__all__'

    @staticmethod
    def get_form_schema():
        """Generate form schema for Alarmplan model."""
        factory = get_form_factory('single')
        creator = factory.create_form_creator(
            model_class=Alarmplan,
            form_id="alarmplan_form",
            form_title="Alarm Plan Form"
        )
        
        config = {
            'categories': [
                {
                    'key': 'plan_details',
                    'title': 'Plan Details',
                    'fields': ['Active', 'RelatedBranch']
                }
            ]
        }
        
        creator.configure_from_dict(config)
        return creator.build()


class ContactPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPerson
        fields = ("ContactPersonName", "ContactPersonPhoneNumber", "ContactPersonEmail", "ContactType")
        extra_kwargs = {
            'ContactPersonName': {'required': True},
            'ContactType': {'required': True}
        }
        read_only_fields = ('RelatedBranch',)

    @staticmethod
    def get_form_schema():
        """Generate form schema for ContactPerson model."""
        factory = get_form_factory('single')
        creator = factory.create_form_creator(
            model_class=ContactPerson,
            form_id="contact_person_form",
            form_title="Contact Person Form"
        )
        
        config = {
            'categories': [
                {
                    'key': 'contact_info',
                    'title': 'Contact Information',
                    'fields': ['ContactPersonName', 'ContactPersonEmail', 'ContactPersonPhoneNumber']
                },
                {
                    'key': 'classification',
                    'title': 'Classification',
                    'fields': ['ContactType']
                }
            ]
        }
        
        creator.configure_from_dict(config)
        return creator.build()

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
            form_id="emergency_planning_form",
            form_title="Emergency Planning Form"
        )
        
        config = {
            'categories': [
                {
                    'key': 'plan_setup',
                    'title': 'Plan Setup',
                    'fields': [
                        {'model': 'Alarmplan', 'field': 'Active'},
                        {'model': 'Alarmplan', 'field': 'RelatedBranch'}
                    ]
                },
                {
                    'key': 'emergency_contacts',
                    'title': 'Emergency Contacts',
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