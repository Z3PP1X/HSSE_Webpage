
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { GoogleMapsModule } from '@angular/google-maps';


import { Component, Input } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { QuestionBase } from '../question-base';




@Component({
  selector: 'app-dynamic-form-question',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule,
            MatInputModule, MatFormFieldModule,
            MatSelectModule, MatDatepickerModule,
            MatNativeDateModule, GoogleMapsModule],

  providers: [MatDatepickerModule],
  templateUrl: './dynamic-form-question.component.html',
  styleUrl: './dynamic-form-question.component.css'
})
export class DynamicFormQuestionComponent {

  @Input() question!: QuestionBase<string>;
  @Input() form!: FormGroup;


  get isValid() {
    return true;
  }


}


// this.form.controls[this.question.key].valid
