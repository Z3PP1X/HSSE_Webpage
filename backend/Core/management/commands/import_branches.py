"""
This command takes the looker export from the active brancehs in germany and updates the internal database.
"""

import json
from django.core.management.base import BaseCommand
from EnterpriseProfile.branchNetwork.BranchNetwork import BranchNetwork

class Command(BaseCommand):
    """Import json branch data to the model"""

    def handle(self, *args, **options):
        payload = options.get('payload')

        try:
            data = json.loads(payload)

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