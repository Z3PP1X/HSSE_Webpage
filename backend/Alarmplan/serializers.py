from rest_framework import serializers
from .models import Alarmplan, ContactPerson
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork

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