from django.contrib.auth import get_user_model
from django.test import TestCase
from ..hsseModules.FirstAidRecord import FirstAidRecord
from django.utils import timezone
import uuid


class TestFirstAidRecord(TestCase):
    """Test creating a record in the first aid record database."""

    def test_create_first_aid_record(self):
        """Test creating a first aid record."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        currentTime = timezone.now()

        first_aid_record = FirstAidRecord.objects.create(
            RequestedFor=user,
            IncidentDateTime=currentTime,
            TypeOfIncident=1,
            InjuryOccurence=True,
            AccidentCause=1,
            PersonalProtectiveEquipment=1,
            WorkContinuation=True,
        )

        self.assertEqual(first_aid_record.RequestedFor, user)
        self.assertEqual(first_aid_record.IncidentDateTime, currentTime)
        self.assertEqual(first_aid_record.TypeOfIncident, 1)
        self.assertEqual(first_aid_record.InjuryOccurence, True)
        self.assertEqual(first_aid_record.AccidentCause, 1)
        self.assertEqual(first_aid_record.PersonalProtectiveEquipment, 1)
        self.assertEqual(first_aid_record.WorkContinuation, True)
        self.assertIsNotNone(first_aid_record.sys_id)
        self.assertTrue(isinstance(first_aid_record.sys_id, uuid.UUID))
        self.assertEqual(first_aid_record.Active, True)

    def test_foreign_key_set_null_on_user_delete(self):
        """Test that a record is set to null when the user is deleted."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        currentTime = timezone.now()

        first_aid_record = FirstAidRecord.objects.create(
            RequestedFor=user,
            IncidentDateTime=currentTime,
            TypeOfIncident=1,
            InjuryOccurence=True,
            AccidentCause=1,
            PersonalProtectiveEquipment=1,
            WorkContinuation=True,
        )
        user.delete()
        first_aid_record.refresh_from_db()
        self.assertIsNone(first_aid_record.RequestedFor)
