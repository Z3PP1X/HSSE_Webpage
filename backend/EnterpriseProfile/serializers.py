from rest_framework import serializers
from .models import BranchNetwork

class BranchUpdateSerializer(serializers.ModelSerializer):

    class Meta: 
        model = BranchNetwork
        fields = ('CostCenter', 'BranchName', 'MandantID', 
                  'RegionID', 'RegionName', 'Country', 'Latitude',
                  'Longitude', 'State', 'City', 'Street', 'PostCode',
                  'BranchOperator', 'BranchMainType')

        


