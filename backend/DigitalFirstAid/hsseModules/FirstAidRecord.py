from django.db import models
from abstractModels import TableModel
from django.contrib.auth.models import User

class FirstAidRecord (TableModel.Table):

    Active = models.BooleanField(default=True),
    RequestedFor = models.ForeignKey(User, null=False, on_delete=models.SET_NULL)
    IncidentDateTime = models.DateTimeField(null=False)
    RequestedForManager = models.ForeignKey(null=False)

    class TypeOfIncident(models.IntegerChoices):
        
        COMMUTE = 1, "Commute"
        WORKPLACE = 2, "Workplace"

    TypeOfIncident = models.IntegerField(choices=TypeOfIncident.choices)
    IncidentLocation = models.JSONField(null=False)
    InjuryOccurence = models.BooleanField(default=False)

    ## First Aid Measures

    AccidentWitness = models.JSONField()
    AffectedBodyParts = models.JSONField()
    UsedBandageMaterial = models.JSONField()

    ## Accident Description

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

    class PersonalProtectiveEquipment(models.IntegerChoices):

        TEST = 1, "Test"

    AccidentCause = models.IntegerField(choices=AccidentCause.choices)
    PersonalProtectiveEquipment = models.IntegerField(choices = PersonalProtectiveEquipment.choices)
    WorkContunuation = models.BooleanField(null=False)









    