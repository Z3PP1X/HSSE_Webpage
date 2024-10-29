from django.db import models
from Core.abstractModels import tableModel
from django.contrib.auth import get_user_model


class FirstAidRecord (tableModel.Table):
    """First Aid Record Model"""
    Active = models.BooleanField(default=True)
    RequestedFor = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    IncidentDateTime = models.DateTimeField(null=False, blank=False)

    class TypeOfIncident(models.IntegerChoices):
        COMMUTE = 1, "Commute"
        WORKPLACE = 2, "Workplace"

    TypeOfIncident = models.IntegerField(
                    choices=TypeOfIncident.choices,
                    blank=False)
    IncidentLocation = models.JSONField(blank=False, default=dict)
    InjuryOccurence = models.BooleanField()

    class AccidentCause(models.IntegerChoices):

        DAMAGEDFURNITURE = 1, "Damaged Furniture"
        EMERGENGYEXIT = 2, "Emergency exits blocked"
        FALLINGOBJECT = 3, "Falling object"
        LIGHTING = 4, "Inadequate lighting"
        CABLE = 5, "Loose cables"
        OBSTRUCTEDPATH = 6, "Obstructed path"
        SLIPPERYFLOORS = 7, "Slippery floors"
        TRIPPINGHAZARD = 8, "Tripping Hazard"
        UNSECUREDOPENING = 9, "Unsecured floor opening"
        SHELVING = 10, "Unstable shelving"

    AccidentDescription = models.TextField(blank=False)

    AccidentWitness = models.JSONField(null=True)
    FirstAidMeasures = models.JSONField(null=True)

    class PersonalProtectiveEquipment(models.IntegerChoices):

        NOEQUIPMENT = 0, "No Equipment"
        GLOVES = 1, "Gloves"
        GLASSES = 2, "Glasses"
        SAFETYWEST = 3, "High-Visibility West"
        MASK = 4, "Mask"
        SAFETYSHOES = 5, "Safety Shoes"
        HARDHAT = 6, "Hard Hat"
        HEARINGPROTECTION = 7, "Hearing Protection"

    AccidentCause = models.IntegerField(choices=AccidentCause.choices)
    PersonalProtectiveEquipment = models.IntegerField(
        choices=PersonalProtectiveEquipment.choices, blank=False, null=True)
    WorkContinuation = models.BooleanField()
