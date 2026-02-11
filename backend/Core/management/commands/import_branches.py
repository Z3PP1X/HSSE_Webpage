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
    help = "Imports branch data from csv"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Pfad zur CSV-Datei')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            # Encoding utf-8 (da du den BOM mit sed entfernt hast)
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                
                # DER FIX: Header säubern (Leerzeichen & BOM entfernen)
                reader.fieldnames = [name.strip().replace('\ufeff', '') for name in reader.fieldnames]
                
                data = list(reader)

            if not data:
                self.stdout.write(self.style.WARNING("Die Datei ist leer."))
                return
            
            self.stdout.write(f"Säuberung abgeschlossen. Spalten erkannt: {reader.fieldnames}")

            # Phase 1: Import unique BG Regions
            region_cache = self._import_regions(data)

            # Phase 2: Import Branches
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

        for entry in data:
            # Nutzung von .strip() beim Key-Zugriff zur Sicherheit
            entity_code = entry.get("Contract Legal Entity Code", "").strip()
            
            if entity_code and entity_code not in unique_region_data:
                unique_region_data[entity_code] = {
                    "Contract_Legal_Name": entry.get("Contract Legal Entity: Name", "").strip(),
                    "Company_Number": entry.get("Unternehmensnummer", "").strip(),
                }

        for entity_code, defaults in unique_region_data.items():
            bg_region, created = BGRegion.objects.update_or_create(
                Entity_Code=entity_code,
                defaults=defaults
            )
            region_cache[entity_code] = bg_region
            action = "Created" if created else "Updated"
            # Optional: Log output reduzieren, falls zu viele Daten
            # self.stdout.write(f"Region {action}: {bg_region.Contract_Legal_Name}")

        return region_cache

    def _import_branches(self, data, region_cache):
        """Processes branches and links them to pre-loaded regions."""
        self.stdout.write("Phase 2: Importing Branches...")
        
        for entry in data:
            # WICHTIG: Hier greifen wir auf die gesäuberten Keys zu
            try:
                branch_id = entry["Branch ID"] # Sollte jetzt existieren!
            except KeyError:
                self.stderr.write(f"Skipping row, missing Branch ID: {entry}")
                continue

            branch, created = BranchNetwork.objects.update_or_create(
                CostCenter=branch_id,
                defaults={
                    "BranchName": entry.get("Branch Name", ""),
                    "RegionID": entry.get("Region ID", ""),
                    "MandantID": entry.get("Mandant ID", ""),
                    "RegionName": entry.get("Region Name", ""),
                    "Country": entry.get("Country", ""),
                    "Latitude": entry.get("Latitude", ""),
                    "Longitude": entry.get("Longitude", ""),
                    "State": entry.get("State", ""),
                    "City": entry.get("City", ""),
                    "Street": entry.get("Street", ""),
                    "PostCode": entry.get("Post Code", ""),
                    "BranchOperator": entry.get("Branch Operator", "")
                }
            )

            # Link branch to region
            entity_code = entry.get("Contract Legal Entity Code", "").strip()
            if entity_code and entity_code in region_cache:
                branch.bg_regions.add(region_cache[entity_code])

            action = "Created" if created else "Updated"
            self.stdout.write(f"Branch {action}: {branch.BranchName}")