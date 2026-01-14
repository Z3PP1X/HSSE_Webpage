"""
This command takes the looker export from the active
branches in germany and updates the internal database.
"""

import csv
from django.core.management.base import BaseCommand
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork


class Command(BaseCommand):
    """Import json branch data to the model"""
    help = "Imports branch data from csv"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Pfad zur CSV-Datei')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:

                reader = csv.DictReader(file, delimiter=';')

            for entry in reader:
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
                action = "Created" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(
                        f"{action}: {branch.BranchName}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Datei nicht gefunden: {file_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
