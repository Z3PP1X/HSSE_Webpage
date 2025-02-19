"""
This command takes the looker export from the active brancehs in germany and updates the internal database.
"""

import json
from django.core.management.base import BaseCommand
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork

class Command(BaseCommand):

    help = "Import branch data from looker Export. NOTE: File has to be in JSON Format"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to JSON file")

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]

        try:
            with open(json_file, "r") as file:
                data = json.load(file)

                for entry in data:
                    branch, created = BranchNetwork.objects.update_or_create(
                        CostCenter=entry["Branch ID"],
                        defaults={

                            "BranchName": entry["Branch Name"],
                            "RegionID": entry["Region ID"],
                            "MandantID": entry["Mandant ID"],
                            "RegionName":entry["Region Name"],
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
                    self.stdout.write(self.style.SUCCESS(f"{action}: {branch.BranchName}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))