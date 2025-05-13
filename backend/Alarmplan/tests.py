from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from EnterpriseProfile.branchNetwork import BranchNetwork
from .models import ContactType, Alarmplan, ContactPerson

class ContactTypeTestCase(TestCase):
    """Tests for ContactType enum"""
    
    def test_contact_type_choices(self):
        """Test that ContactType has the correct choices"""
        self.assertEqual(ContactType.FIRSTAID, 1)
        self.assertEqual(ContactType.BRANCH_MANAGER, 2)
        self.assertEqual(ContactType.INTERNAL, 3)
        self.assertEqual(ContactType.EXTERNAL, 4)
        
        self.assertEqual(ContactType.choices[0][1], "Emergency")
        self.assertEqual(ContactType.choices[1][1], "Non-Emergency")
        self.assertEqual(ContactType.choices[2][1], "Internal")
        self.assertEqual(ContactType.choices[3][1], "External")


class AlarmplanTestCase(TestCase):
    """Tests for Alarmplan model"""
    
    def setUp(self):
        """Set up test data"""
        self.branch = BranchNetwork.objects.create(
            name="Test Branch"
            
        )
    
    def test_create_alarmplan(self):
        """Test creating an Alarmplan instance"""
        alarmplan = Alarmplan.objects.create(
            Active=True,
            RelatedBranch=self.branch
        )
        
        self.assertTrue(alarmplan.Active)
        self.assertEqual(alarmplan.RelatedBranch, self.branch)
        
    def test_inactive_alarmplan(self):
        """Test creating an inactive Alarmplan"""
        alarmplan = Alarmplan.objects.create(
            Active=False,
            RelatedBranch=self.branch
        )
        
        self.assertFalse(alarmplan.Active)
        
    def test_alarmplan_without_branch(self):
        """Test creating an Alarmplan without a branch"""
        alarmplan = Alarmplan.objects.create(
            Active=True,
            RelatedBranch=None
        )
        
        self.assertIsNone(alarmplan.RelatedBranch)


class ContactPersonTestCase(TestCase):
    """Tests for ContactPerson model"""
    
    def setUp(self):
        """Set up test data"""
        self.branch = BranchNetwork.objects.create(
            CostCenter="12345",
            Active=True,
            BranchName="Test Branch",
            MandantID="M001",
            RegionID="R001",
            RegionName="Test Region",
            Country="Germany",
            Latitude="53.56764",
            Longitude="13.26991",
            State="Bavaria",
            City="Munich",
            Street="Test Street 123",
            PostCode="80331",
            BranchOperator="Corporate Branch",
            BranchMainType="Downtown"
        )
    
    def test_create_contact_person_with_email(self):
        """Test creating a ContactPerson with email only"""
        contact = ContactPerson.objects.create(
            RelatedBranch=self.branch,
            ContactPersonName="John Doe",
            ContactPersonEmail="john@example.com",
            ContactType=ContactType.FIRSTAID
        )
        
        self.assertEqual(contact.ContactPersonName, "John Doe")
        self.assertEqual(contact.ContactPersonEmail, "john@example.com")
        self.assertEqual(contact.ContactType, ContactType.FIRSTAID)
        
    def test_create_contact_person_with_phone(self):
        """Test creating a ContactPerson with phone only"""
        contact = ContactPerson.objects.create(
            RelatedBranch=self.branch,
            ContactPersonName="Jane Smith",
            ContactPersonPhoneNumber="+49123456789",
            ContactType=ContactType.BRANCH_MANAGER
        )
        
        self.assertEqual(contact.ContactPersonName, "Jane Smith")
        self.assertEqual(contact.ContactPersonPhoneNumber, "+49123456789")
        self.assertEqual(contact.ContactType, ContactType.BRANCH_MANAGER)
    
    def test_create_contact_person_with_both(self):
        """Test creating a ContactPerson with both email and phone"""
        contact = ContactPerson.objects.create(
            RelatedBranch=self.branch,
            ContactPersonName="Alice Brown",
            ContactPersonEmail="alice@example.com",
            ContactPersonPhoneNumber="+49987654321",
            ContactType=ContactType.INTERNAL
        )
        
        self.assertEqual(contact.ContactPersonName, "Alice Brown")
        self.assertEqual(contact.ContactPersonEmail, "alice@example.com")
        self.assertEqual(contact.ContactPersonPhoneNumber, "+49987654321")
        self.assertEqual(contact.ContactType, ContactType.INTERNAL)
    
    def test_contact_without_email_or_phone(self):
        """Test that ValidationError is raised when neither email nor phone is provided"""
        with self.assertRaises(ValidationError):
            ContactPerson.objects.create(
                RelatedBranch=self.branch,
                ContactPersonName="Bob White",
                ContactType=ContactType.EXTERNAL
            )