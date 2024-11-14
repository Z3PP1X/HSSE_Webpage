import { Component, input, Input, OnInit, WritableSignal } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormConfig } from './SubmittableForm.model';
import { QuestionBase } from '../../DynamicForms/question-base';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { QuestionControlService } from '../../DynamicForms/question-control.service';



@Component({
  selector: 'app-submittable-form-card',
  standalone: true,
  imports: [MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './submittable-form-card.component.html',
  styleUrl: './submittable-form-card.component.scss',
})
export class SubmittableFormCardComponent implements OnInit {
  configurationItem = input<FormConfig[]>();
  formTitle = input.required<string>();

  @Input() questions: QuestionBase<string>[] | null = [];
  form!: FormGroup;
  payLoad = '';

  constructor(private qcs: QuestionControlService) {}

  ngOnInit() {
    this.form = this.qcs.toFormGroup(this.questions as QuestionBase<string>[]);
  }

  onSubmit() {
    this.payLoad = JSON.stringify(this.form.getRawValue());
  }


}
