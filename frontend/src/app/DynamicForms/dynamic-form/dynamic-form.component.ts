import { Component, Input, OnChanges, OnInit, SimpleChanges, input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';

import { DynamicFormQuestionComponent } from '../dynamic-form-question/dynamic-form-question.component';

import { QuestionBase } from '../question-base';
import { QuestionControlService } from '../question-control.service';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { Observable, of, Subscription} from 'rxjs';



@Component({
  selector: 'app-dynamic-form',
  standalone: true,
  providers: [QuestionControlService],
  imports: [CommonModule, DynamicFormQuestionComponent, ReactiveFormsModule, MatCardModule, MatButtonModule],
  templateUrl: './dynamic-form.component.html',
  styleUrl: './dynamic-form.component.css'
})
export class DynamicFormComponent implements OnInit{

  formTitle = input.required<string>();
  @Input() questions: QuestionBase<string>[] | null = [];
  form!: FormGroup;
  payLoad = '';

  constructor(private qcs: QuestionControlService) {}

  ngOnInit(): void {
        console.log("MOOOIN", this.questions)
        this.form = this.qcs.toFormGroup(this.questions as QuestionBase<string>[]);
      }

  onSubmit() {
    this.payLoad = JSON.stringify(this.form.getRawValue());
  }

}
