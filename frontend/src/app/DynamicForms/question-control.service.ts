import { Injectable } from "@angular/core";
import { FormControl, FormGroup, Validators } from "@angular/forms";

import { QuestionBase } from "./question-base";

@Injectable()
export class QuestionControlService {
  toFormGroup(questions: QuestionBase<string>[]) {
    const group: any = {};

    questions.forEach((question) => {
      if (question.key) {
        group[question.key] = question.required
          ? new FormControl(question.key || '', Validators.required)
          : new FormControl(question.key || '');
      } else {
        console.error('Missing key for question:', question);  
      }
    });
    console.log('Form Group:', group);

    return new FormGroup(group);
  }
}
