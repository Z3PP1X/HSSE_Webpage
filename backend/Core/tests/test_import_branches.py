import io
from django.core.management import call_command
from django.test import TestCase
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork
from EnterpriseProfile.branchNetwork.BGRegion import BGRegion
from unittest.mock import patch

class ImportBranchesTest(TestCase):
    """Test the import_branches management command."""

    def setUp(self):
        # Sample CSV content using semicolon delimiter
        self.csv_headers = (
            "Branch ID;Branch Name;Region ID;Mandant ID;Region Name;Country;"
            "Latitude;Longitude;State;City;Street;Post Code;Branch Operator;"
            "Entity_Code;Contract_Legal_Name;Company_Number\n"
        )
        self.row1 = "001;Munich Airport;R1;M1;Bavaria;Germany;48.35;11.78;Bavaria;Freising;Airport Ave;85356;Sixt;EC1;Sixt GmbH;123\n"
        self.row2 = "002;Berlin Center;R2;M1;Berlin;Germany;52.52;13.40;Berlin;Berlin;Leipziger Str;10117;Sixt;EC1;Sixt GmbH;123\n"
        self.row3 = "003;Hamburg Port;R3;M1;Hamburg;Germany;53.55;9.99;Hamburg;Hamburg;Port St;20457;Sixt;EC2;Sixt North;456\n"
        self.csv_content = self.csv_headers + self.row1 + self.row2 + self.row3

    def test_import_branches_success(self):
        """Test that regions and branches are imported correctly and linked."""
        # Use StringIO to simulate the file content
        with patch("Core.management.commands.import_branches.open", return_value=io.StringIO(self.csv_content)):
            call_command('import_branches', 'dummy.csv')

        # Verify Regions (Phase 1 result)
        # Should have 2 unique regions: EC1 and EC2
        self.assertEqual(BGRegion.objects.count(), 2)
        
        region_ec1 = BGRegion.objects.get(Entity_Code="EC1")
        self.assertEqual(region_ec1.Contract_Legal_Name, "Sixt GmbH")
        self.assertEqual(region_ec1.Company_Number, "123")
        
        region_ec2 = BGRegion.objects.get(Entity_Code="EC2")
        self.assertEqual(region_ec2.Contract_Legal_Name, "Sixt North")
        self.assertEqual(region_ec2.Company_Number, "456")

        # Verify Branches (Phase 2 result)
        self.assertEqual(BranchNetwork.objects.count(), 3)
        
        # Branch 001 linked to EC1
        branch001 = BranchNetwork.objects.get(CostCenter="001")
        self.assertEqual(branch001.BranchName, "Munich Airport")
        self.assertTrue(branch001.bg_regions.filter(Entity_Code="EC1").exists())
        
        # Branch 002 also linked to EC1
        branch002 = BranchNetwork.objects.get(CostCenter="002")
        self.assertEqual(branch002.BranchName, "Berlin Center")
        self.assertTrue(branch002.bg_regions.filter(Entity_Code="EC1").exists())
        
        # Branch 003 linked to EC2
        branch003 = BranchNetwork.objects.get(CostCenter="003")
        self.assertTrue(branch003.bg_regions.filter(Entity_Code="EC2").exists())

    def test_import_branches_updates_existing(self):
        """Test that the command updates existing records instead of duplicating."""
        # Pre-create a region and a branch
        BGRegion.objects.create(Entity_Code="EC1", Contract_Legal_Name="Old Name", Company_Number="000")
        BranchNetwork.objects.create(CostCenter="001", BranchName="Old Branch")

        with patch("Core.management.commands.import_branches.open", return_value=io.StringIO(self.csv_content)):
            call_command('import_branches', 'dummy.csv')

        # Counts should still be correct
        self.assertEqual(BGRegion.objects.count(), 2)
        self.assertEqual(BranchNetwork.objects.count(), 3)

        # Region should be updated
        region_ec1 = BGRegion.objects.get(Entity_Code="EC1")
        self.assertEqual(region_ec1.Contract_Legal_Name, "Sixt GmbH")
        self.assertEqual(region_ec1.Company_Number, "123")

        # Branch should be updated
        branch001 = BranchNetwork.objects.get(CostCenter="001")
        self.assertEqual(branch001.BranchName, "Munich Airport")
