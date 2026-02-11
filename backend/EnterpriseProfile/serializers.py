from rest_framework import serializers
from .models import BranchNetwork
from .branchNetwork.BGRegion import BGRegion


class BGRegionSerializer(serializers.ModelSerializer):
    """Serializer for BGRegion model."""

    class Meta:
        model = BGRegion
        fields = ('sys_id', 'Contract_Legal_Name', 'Entity_Code', 'Company_Number')


class BranchUpdateSerializer(serializers.ModelSerializer):
    """Serializer for BranchNetwork model with nested regions."""

    bg_regions = BGRegionSerializer(many=True, read_only=True)

    class Meta:
        model = BranchNetwork
        fields = ('CostCenter', 'BranchName', 'MandantID',
                  'RegionID', 'RegionName', 'Country', 'Latitude',
                  'Longitude', 'State', 'City', 'Street', 'PostCode',
                  'BranchOperator', 'BranchMainType', 'bg_regions')
