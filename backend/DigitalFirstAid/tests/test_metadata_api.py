"""
Tests for the first aid book metadata api.
"""

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from DigitalFirstAid.serializers import FirstAidRecordSerializer

DIGITAL_FIRST_AID_BOOK_URL = reverse('digitalfirstaid:metadata')


class MetadataTest(TestCase):
    """Test the metadata API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_model_metadata(self):
        "Retrieving model data form the metadata endpoint."






