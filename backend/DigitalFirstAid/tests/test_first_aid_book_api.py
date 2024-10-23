"""
Tests for digital first aid book APIs.
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


from ..hsseModules.FirstAidRecord import FirstAidRecord

from DigitalFirstAid.serializers import FirstAidRecordSerializer

DIGITAL_FIRST_AID_BOOK_URL = reverse('digitalfirstaid:firstaidrecord-list')


def create_first_aid_record(user, **params):
    """Create a first aid record."""

    currentTime = timezone.now()

    defaults = {
        'RequestedFor': user,
        'IncidentDateTime': currentTime,
        'TypeOfIncident': 1,
        'InjuryOccurence': True,
        'AccidentCause': 1,
        'PersonalProtectiveEquipment': 1,
        'WorkContinuation': True,
    }
    defaults.update(params)
    first_aid_record = FirstAidRecord.objects.create(**defaults)
    return first_aid_record


class PublicFirstAidRecordAPITests(TestCase):
    """Test unauthenticated first aid record API access."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(DIGITAL_FIRST_AID_BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFirstAidRecordAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_first_aid_records(self):
        """Test retrieving a list of first aid records."""
        create_first_aid_record(user=self.user)
        create_first_aid_record(user=self.user)

        res = self.client.get(DIGITAL_FIRST_AID_BOOK_URL)

        first_aid_record = FirstAidRecord.objects.all().order_by('-created_on')
        serializer = FirstAidRecordSerializer(first_aid_record, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test that only records for authenticated user are returned."""

        user2 = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
            )
        create_first_aid_record(user=user2)
        create_first_aid_record(user=self.user)

        res = self.client.get(DIGITAL_FIRST_AID_BOOK_URL)

        first_aid_record = FirstAidRecord.objects.filter(
            RequestedFor=self.user)
        serializer = FirstAidRecordSerializer(first_aid_record, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
