from django.db import models
from Core.abstractModels import tableModel
from django.contrib.auth import get_user_model
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork
from django.core.exceptions import ValidationError


class ContactType(models.IntegerChoices):
    """Contact Type Model"""
    FIRSTAID = 1, "Emergency"
    BRANCH_MANAGER = 2, "Non-Emergency"
    INTERNAL = 3, "Internal"
    EXTERNAL = 4, "External"

class Alarmplan(tableModel.Table):
    """Alarmplan Model"""
    Active = models.BooleanField(default=True)
    RelatedBranch = models.ForeignKey(BranchNetwork, null=True, on_delete=models.SET_NULL)
    contactPerson = models.ManyToManyField("ContactPerson")
    AssemblyPoint = models.CharField(max_length=255, blank=True)
    PoisonEmergencyHotline = models.CharField(max_length=255, blank=True)


class ContactPerson(tableModel.Table):
    """Contact Person Model"""
    RelatedBranch = models.ForeignKey(BranchNetwork, null=True, on_delete=models.SET_NULL)
    ContactPersonName = models.CharField(max_length=255, blank=False)
    ContactPersonPhoneNumber = models.IntegerField(max_length=255, blank=True)
    ContactPersonEmail = models.EmailField(blank=True)
    ContactType = models.IntegerField(blank=False, choices=ContactType.choices)

    def clean(self):
        """Ensure that either email or phone number is provided."""

        if not self.ContactPersonPhoneNumber and not self.ContactPersonEmail:
            raise ValidationError("Either phone number or email must be provided.")

        super().clean()

    def save(self, *args, **kwargs):
        """Call clean before saving to ensure validation."""
        self.clean()
        super().save(*args, **kwargs)



