export const TESTQUESTIONS = [
  {
    "key": "RequestedFor",
    "label": "Requested For",
    "value": 0,
    "required": true,
    "controlType": "textbox",
    "type": "text",
    "order": 1,
    "options": []
  },
  {
    "key": "IncidentDateTime",
    "label": "When did the incident occur?",
    "value": 0,
    "required": true,
    "controlType": "textbox",
    "type": "datetime-local",
    "order": 2,
    "options": []
  },
  {
    "key": "TypeOfIncident",
    "label": "Did the incident occur during commute or at the workplace?",
    "value": 0,
    "required": true,
    "controlType": "textbox",
    "type": "",
    "order": 3,
    "options": [
      { "key": "1", "value": 1 },
      { "key": "2", "value": 2 }
    ]
  },
  {
    "key": "IncidentLocation",
    "label": "Where did the incident occur?",
    "value": 0,
    "required": true,
    "controlType": "textbox",
    "type": "text",
    "order": 4,
    "options": []
  },
  {
    "key": "InjuryOccurence",
    "label": "Did the incident result in an injury?",
    "value": 0,
    "required": true,
    "controlType": "dropdown",
    "type": "",
    "order": 5,
    "options": [
      { "key": "true", "value": 1 },
      { "key": "false", "value": 2 }
    ]
  },
  {
    "key": "AccidentDescription",
    "label": "Please describe the incident",
    "value": 0,
    "required": true,
    "controlType": "textbox",
    "type": "textarea",
    "order": 6,
    "options": []
  },
  {
    "key": "AccidentCause",
    "label": "What caused the accident?",
    "value": 0,
    "required": true,
    "controlType": "dropdown",
    "type": "",
    "order": 7,
    "options": [
      { "key": "1", "value": 1 },
      { "key": "2", "value": 2 },
      { "key": "3", "value": 3 },
      { "key": "4", "value": 4 },
      { "key": "5", "value": 5 },
      { "key": "6", "value": 6 },
      { "key": "7", "value": 7 },
      { "key": "8", "value": 8 },
      { "key": "9", "value": 9 },
      { "key": "10", "value": 10 }
    ]
  },
  {
    "key": "PersonalProtectiveEquipment",
    "label": "What protective equipment was used?",
    "value": 0,
    "required": false,
    "controlType": "dropdown",
    "type": "",
    "order": 8,
    "options": [
      { "key": "0", "value": 0 },
      { "key": "1", "value": 1 },
      { "key": "2", "value": 2 },
      { "key": "3", "value": 3 },
      { "key": "4", "value": 4 },
      { "key": "5", "value": 5 },
      { "key": "6", "value": 6 },
      { "key": "7", "value": 7 }
    ]
  },
  {
    "key": "WorkContinuation",
    "label": "Was work continued after the incident?",
    "value": 0,
    "required": true,
    "controlType": "dropdown",
    "type": "",
    "order": 9,
    "options": [
      { "key": "true", "value": 1 },
      { "key": "false", "value": 2 }
    ]
  }
]
