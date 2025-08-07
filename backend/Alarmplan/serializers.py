from rest_framework import serializers
from .models import Alarmplan, ContactPerson
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork
from JsonSchemaForms.model_schema_builder import ModelFormSchemaBuilder

class AlarmplanSerializer(serializers.ModelSerializer):
    RelatedBranch = serializers.SlugRelatedField(
            slug_field='CostCenter',
            queryset=BranchNetwork.objects.all()
        )
    class Meta:
        model = Alarmplan
        fields = '__all__'


class ContactPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPerson
        fields = ("ContactPersonName", "ContactPersonPhoneNumber", "ContactPersonEmail", "ContactType")
        extra_kwargs = {
            'ContactPersonName': {'required': True},
            'ContactType': {'required': True}
        }
        read_only_fields = ('RelatedBranch',)


class AlarmplanSerializer(serializers.BaseSerializer):
    """Serializer for the Alarmplan Model"""

    def get_model_metadata(model, meta_whitelist=[]):

        builder = ModelFormSchemaBuilder(
            model_class=model,
            form_id="alarmplan_generation_form",
            form_title="Alarmplan"
        )

        config = {
            'categories': [
                {
                    'key': 'branch_location',
                    'title': 'Branch Location',
                    'fields': ['RelatedBranch']
                },
                {
                    'key': 'first_aid_contacts',
                    'title': 'First Aiders',
                    'fields': []
                },
            ]

        }

        builder.configure_from_dict(config)


        return builder.build()