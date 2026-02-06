"""
Business Group Region / Legal Entity Model.

This model represents the legal entities and regions that branches
are associated with. Each region has a unique Entity_Code and can
be linked to multiple branches via M2M relationship.
"""

from django.db import models
from Core.abstractModels import tableModel


class BGRegion(tableModel.Table):
    """
    Business Group Region / Legal Entity Model.

    Attributes:
        Contract_Legal_Name: The official legal name of the entity.
        Entity_Code: Unique identifier for the entity.
        Company_Number: The company registration number.
    """

    Contract_Legal_Name = models.CharField(max_length=255)
    Entity_Code = models.CharField(max_length=50, unique=True)
    Company_Number = models.CharField(max_length=50)

    class Meta:
        verbose_name = "BG Region"
        verbose_name_plural = "BG Regions"

    def __str__(self) -> str:
        """Return string representation of the region."""
        return f"{self.Contract_Legal_Name} ({self.Entity_Code})"
