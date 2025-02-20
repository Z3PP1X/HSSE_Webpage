from django.db import models
from Core.abstractModels import tableModel

class BranchNetwork(tableModel.Table):
    """Branch Network Model"""

    CostCenter = models.CharField(max_length=5, unique=True)
    Active = models.BooleanField(default=True)
    BranchName = models.CharField(max_length=100)

    ### Location Specific Fields:

    MandantID = models.CharField(max_length=50)
    RegionID = models.CharField(max_length=50)
    RegionName = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Latitude = models.CharField()
    Longitude = models.CharField()
    State = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    PostCode = models.CharField(max_length=10)
    BranchOperator = models.CharField(max_length=50)

    ### Branch Type

    BranchMainType = models.CharField(max_length=100)

    ### Safety Aspects

    AssemblyPoint = models.CharField(blank=True)
    PoisonEmergencyCallNumber = models.CharField(blank=True)