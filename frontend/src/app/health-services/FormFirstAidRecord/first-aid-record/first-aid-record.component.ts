import { DUMMY_QUESTIONS_ALT } from './../../../../dummy-questions2';
import { Component, DestroyRef, OnInit, inject } from '@angular/core';
import { SubmittableFormCardComponent } from '../../../components/submittable-form-card/submittable-form-card.component';
import { AbstractControl, FormControl,  FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { debounceTime } from 'rxjs';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';

interface TypeOfIncident {
  value: number;
  viewValue: string;
}

function mustContainQuestion(control: AbstractControl) {
  if (control.value.includes('?')) {
    return null;
  }

  return { doesNotContainQuestion: true};
}


@Component({
  selector: 'app-first-aid-record',
  standalone: true,
  imports: [SubmittableFormCardComponent, ReactiveFormsModule, MatSelectModule, MatFormFieldModule, MatInputModule, MatDatepickerModule],
  templateUrl: './first-aid-record.component.html',
  styleUrl: './first-aid-record.component.scss'
})
export class FirstAidRecordComponent implements OnInit{

  private destroyRef = inject(DestroyRef);

  configurationItem = DUMMY_QUESTIONS_ALT;

  formTitle = "Ersthelferbericht";

  TypeOfIncident: TypeOfIncident[] =  [
    {
    value: 1,
    viewValue: "Commute"
  },
  {
    value: 2,
    viewValue: "Workplace"
  }
]




  FirstAidRecord = new FormGroup({

    RequestedFor: new FormControl('', { validators: [Validators.required, Validators.email, Validators.minLength(10)], updateOn: 'blur'}),
    IncidentDateTime: new FormControl('', { validators: [Validators.required], updateOn: 'blur'}),


    IncidentLocations: new FormGroup({
      TypeOfIncident: new FormControl(0, {validators: [Validators.required], updateOn: 'blur'}),
      Street: new FormControl('', {validators: [], updateOn: 'blur'}),
      ZipCode: new FormControl('', {validators: [],}),
      City: new FormControl('', {validators: []}),
      Number: new FormControl('', {validators: []}),

    }),
    InjuryOccurence: new FormControl('', {validators: [Validators.required], updateOn: 'blur'}),
    AccidentCause: new FormControl('', {validators: [], updateOn: 'blur'}),
    AccidentDescription: new FormControl('', {validators: [], updateOn: 'blur'}),
    AccidentWitness: new FormControl('', {validators: [], updateOn: 'blur'}),
    FirstAidMeasures: new FormControl('', {validators: [], updateOn: 'blur'}),
    PersonalProtectiveEquipment: new FormControl('', {validators: [], updateOn: 'blur'}),
    WorkContinuation: new FormControl('', {validators: [], updateOn: 'blur'})



  })

  ngOnInit() {


    const savedForm = window.localStorage.getItem('saved-first-aid-record-form');

    if (savedForm) {
      const loadedForm = JSON.parse(savedForm);
      this.FirstAidRecord.patchValue({
        RequestedFor: loadedForm.RequestedFor
      })
    }
    const subscription = this.FirstAidRecord.valueChanges.pipe(debounceTime(500)).subscribe({

      next: (value) => {
        window.localStorage.setItem(
          'saved-first-aid-record-form',
          JSON.stringify({RequestedFor: value.RequestedFor})
        );
      },

    });
    this.destroyRef.onDestroy(() => subscription.unsubscribe());
  }


}
