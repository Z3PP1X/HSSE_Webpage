export const TESTQUESTIONS = [
  {
    "key": "name",
    "label": "name",
    "value": "",
    "required": true,
    "controlType": "textbox",
    "type": "text",
    "order": 1,
    "options": []
  },
  {
    "key": "email",
    "label": "Email",
    "value": "",
    "required": true,
    "controlType": "textbox",
    "type": "email",
    "order": 2,
    "options": []
  },
  {
    "key": "dob",
    "label": "Date of Birth",
    "value": "",
    "required": false,
    "controlType": "dropdown",
    "type": "date",
    "order": 3,
    "options": []
  },
  {
    "key": "gender",
    "label": "Gender",
    "value": "male",
    "required": false,
    "controlType": "dropdown",
    "type": "",
    "order": 4,
    "options": [
      { "key": "male", "value": "Male" },
      { "key": "female", "value": "Female" },
      { "key": "other", "value": "Other" }
    ]
  },
  {
    "key": "country",
    "label": "Country",
    "value": "",
    "required": true,
    "controlType": "textbox",
    "type": "",
    "order": 5,
    "options": [
      { "key": "de", "value": "Germany" },
      { "key": "us", "value": "USA" },
      { "key": "uk", "value": "UK" }
    ]
  },
  {
    "key": "appointment",
    "label": "Appointment Date and Time",
    "value": "",
    "required": true,
    "controlType": "textbox",
    "type": "datetime-local",
    "order": 6,
    "options": []
  },
  {
    "key": "location",
    "label": "Meeting Location",
    "value": "",
    "required": false,
    "controlType": "location",
    "type": "",
    "order": 7,
    "options": []
  },
  {
    "key": "feedback",
    "label": "Feedback",
    "value": "",
    "required": false,
    "controlType": "textbox",
    "type": "textarea",
    "order": 8,
    "options": []
  },
  {
    "key": "rating",
    "label": "Rating (1-5)",
    "value": "5",
    "required": true,
    "controlType": "textbox",
    "type": "",
    "order": 9,
    "options": [
      { "key": "1", "value": "1" },
      { "key": "2", "value": "2" },
      { "key": "3", "value": "3" },
      { "key": "4", "value": "4" },
      { "key": "5", "value": "5" }
    ]
  },
  {
    "key": "comments",
    "label": "Additional Comments",
    "value": "",
    "required": false,
    "controlType": "textbox",
    "type": "textarea",
    "order": 10,
    "options": []
  }
]
