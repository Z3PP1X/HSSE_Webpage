from django.db import models
from Core.abstractModels import tableModel

class BranchNetwork(tableModel):
    """Branch Network Model"""

    CostCenter = models.CharField(max_length=5, unique=True)
    Active = models.BooleanField(default=True)
    BranchName = models.CharField()

    ### Location Specific Fields:

    RegionID = models.CharField()
    RegionName = models.CharField()
    Country = models.CharField()
    Latitude = models.CharField()
    Longitude = models.CharField()
    State = models.CharField()
    City = models.CharField()
    Street = models.CharField()


    ### Branch Type

    BranchMainType = models.CharField()

    ### Safety Aspects

    AssemblyPoint = models.CharField(null=True)
    PoisonEmergencyCallNumber = models.CharField(null=True)