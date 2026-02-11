"""
This command takes the looker export from the active
branches in germany and updates the internal database.
"""

import csv
import logging
from django.core.management.base import BaseCommand
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork
from EnterpriseProfile.branchNetwork.BGRegion import BGRegion

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Import branch data from CSV with separated logic for Regions and Branches."""
    help = "Imports branch data from csv"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Pfad zur CSV-Datei')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=',')
                data = list(reader)

            # Phase 1: Import unique BG Regions and cache them
            region_cache = self._import_regions(data)

            # Phase 2: Import Branches and link to regions
            self._import_branches(data, region_cache)

            self.stdout.write(self.style.SUCCESS("Successfully imported all data."))

        except FileNotFoundError:
            logger.error(f"Import failed: File not found at {file_path}")
            self.stderr.write(self.style.ERROR(f"Datei nicht gefunden: {file_path}"))
        except Exception as e:
            logger.exception(f"Unexpected error during branch import: {e}")
            self.stderr.write(self.style.ERROR(f"Error: {e}"))

    def _import_regions(self, data):
        """Processes unique regions from the data and returns a lookup cache."""
        self.stdout.write("Phase 1: Importing BG Regions...")
        region_cache = {}
        unique_region_data = {}

        # Collect unique region data to minimize update_or_create calls
        for entry in data:
            # UPDATED KEY: Matches 'Contract Legal Entity Code' from your new CSV
            entity_code = entry.get("Contract Legal Entity Code", "").strip()
            
            if entity_code and entity_code not in unique_region_data:
                unique_region_data[entity_code] = {
                    # UPDATED KEYS: Match 'Contract Legal Entity: Name' and 'Unternehmensnummer'
                    "Contract_Legal_Name": entry.get("Contract Legal Entity: Name", ""),
                    "Company_Number": entry.get("Unternehmensnummer", ""),
                }

        for entity_code, defaults in unique_region_data.items():
            bg_region, created = BGRegion.objects.update_or_create(
                Entity_Code=entity_code,
                defaults=defaults
            )
            region_cache[entity_code] = bg_region
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(
                f"  Region {action}: {bg_region.Contract_Legal_Name} ({entity_code})"
            ))

        return region_cache

    def _import_branches(self, data, region_cache):
        """Processes branches and links them to pre-loaded regions."""
        self.stdout.write("Phase 2: Importing Branches...")
        for entry in data:
            branch, created = BranchNetwork.objects.update_or_create(
                CostCenter=entry["Branch ID"],
                defaults={
                    "BranchName": entry["Branch Name"],
                    "RegionID": entry["Region ID"],
                    "MandantID": entry["Mandant ID"],
                    "RegionName": entry["Region Name"],
                    "Country": entry["Country"],
                    "Latitude": entry["Latitude"],
                    "Longitude": entry["Longitude"],
                    "State": entry["State"],
                    "City": entry["City"],
                    "Street": entry["Street"],
                    "PostCode": entry["Post Code"],
                    "BranchOperator": entry["Branch Operator"]
                }
            )

            # Link branch to region via M2M relationship if cached
            # UPDATED KEY: Must match the column used in _import_regions
            entity_code = entry.get("Contract Legal Entity Code", "").strip()
            
            if entity_code and entity_code in region_cache:
                branch.bg_regions.add(region_cache[entity_code])

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(
                f"  Branch {action}: {branch.BranchName}"
            ))