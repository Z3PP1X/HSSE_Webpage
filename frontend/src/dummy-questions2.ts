export const DUMMY_QUESTIONS_ALT = [
  {
    id: 4,
    title: "Arbeitsschutzmaßnahmen",
    category: [
      {
        id: 4,
        name: "Arbeitsschutzmaßnahmen",
        questions: [
          { sys_id: "q13", label: "Welche Schutzmaßnahmen wurden ergriffen?", validators: [{ required: true }] },
          { sys_id: "q14", label: "Gab es eine Unterweisung vor Beginn der Arbeit?", validators: [{ required: false }] },
          { sys_id: "q15", label: "Wurde persönliche Schutzausrüstung getragen?", validators: [{ required: true }] },
          { sys_id: "q16", label: "Gab es eine Sicherheitsüberprüfung?", validators: [{ required: false }] }
        ]
      }
    ]
  },
  {
    id: 5,
    title: "Maschinenwartungsbericht",
    category: [
      {
        id: 5,
        name: "Maschinenwartungsbericht",
        questions: [
          { sys_id: "q17", label: "Wann fand die letzte Wartung statt?", validators: [{ required: true, DateTime: true }] },
          { sys_id: "q18", label: "Welche Maschinen wurden gewartet?", validators: [{ required: true }] },
          { sys_id: "q19", label: "Gab es Mängel an der Maschine?", validators: [{ required: false }] },
          { sys_id: "q20", label: "Welche Teile wurden ersetzt?", validators: [{ required: false }] }
        ]
      }
    ]
  },
  {
    id: 6,
    title: "Gefahrenstoffbericht",
    category: [
      {
        id: 6,
        name: "Gefahrenstoffbericht",
        questions: [
          { sys_id: "q21", label: "Welche Gefahrstoffe wurden verwendet?", validators: [{ required: true }] },
          { sys_id: "q22", label: "Gab es eine spezielle Lagerung der Stoffe?", validators: [{ required: false }] },
          { sys_id: "q23", label: "Wurde ein Sicherheitsdatenblatt bereitgestellt?", validators: [{ required: true }] },
          { sys_id: "q24", label: "Gab es Unfälle im Umgang mit den Stoffen?", validators: [{ required: false }] }
        ]
      }
    ]
  }
];
