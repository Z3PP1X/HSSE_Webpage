# config.py
ALARMPLAN_FORM_CONFIG = {
    "categories": [
        {
            "key": "Branch",
            "title": "Branch",
            "expandable": False,  # Static category
            "fields": [
                {
                    "model": "Alarmplan",
                    "field": "RelatedBranch",
                    "ajax": {
                        "endpoint": "/api/branchnetwork/costcenters/",
                        "method": "GET",
                        "events": ["input", "focus"],
                        "debounce": 300,
                        "field_type": "ajax_select",
                        "search_field": "CostCenter",
                        "display_field": "BranchName",
                        "value_field": "sys_id"
                    }
                }
            ]
        },
        {
            "key": "Sammelplatz",
            "title": "Sammelplatz",
            "expandable": False,  # Static category
            "fields": [
                {"model": "Alarmplan", "field": "AssemblyPoint", "question": "Sammelplatz"},

            ]
        },
        {
            "key": "Ersthelfer",
            "title": "Ersthelfer",
            "expandable": True,  # Dynamic category - can have multiple instances
            "min_instances": 1,   # Optional: minimum required instances
            "max_instances": 5,  # Optional: maximum allowed instances
            "fields": [
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonName",
                    "question": "Name"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonEmail",
                    "question": "Email"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonPhoneNumber",
                    "question": "Telefonnummer"
                },

            ]
        },
        
        {
            "key": "Nächstes Krankenhaus",
            "title": "Nächstes Krankenhaus",
            "expandable": False, 
            "min_instances": 1,  
            "max_instances": 1,  
            "fields": [
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonName",
                    "question": "Name des Krankenhauses"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonName",
                    "question": "Straße und Hausnummer"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonPhoneNumber",
                    "question": "Postleitzahl"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactType",
                    "question": "Telefonnummer"
                }
            ]
        },
        {
            "key": "Wichtige Kontakte",
            "title": "Wichtige Kontakte",
            "expandable": False,  # Dynamic category - can have multiple instances
            "min_instances": 1,   # Optional: minimum required instances
            "max_instances": 10,  # Optional: maximum allowed instances
            "fields": [
                {
                    "model": "Alarmplan",
                    "field": "PoisonEmergencyHotline",
                    "question": "Nummer des Giftnotrufs"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonName",
                    "question": "Name des Branch Managers",
                    "group": "branchManager"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonEmail",
                    "question": "Email des Branch Managers",
                    "group": "branchManager"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonName",
                    "question": "Name des Geschaftsführers",
                    "group": "management1"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonEmail",
                    "question": "Email des Geschäftsführers",
                    "group": "management1"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonName",
                    "question": "Name des Geschaftsführers",
                    "group": "management2"
                },
                {
                    "model": "ContactPerson",
                    "field": "ContactPersonEmail",
                    "question": "Email des Geschäftsführers",
                    "group": "management2"
                },
            ]
        },
    ]
}
