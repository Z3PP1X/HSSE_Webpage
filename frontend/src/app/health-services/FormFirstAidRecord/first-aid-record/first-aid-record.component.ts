
import { Component,  OnInit, } from '@angular/core';
import { TESTQUESTIONS } from '../../../DynamicForms/TEST-Questions';
import { AsyncPipe } from '@angular/common';

import { DynamicFormComponent } from '../../../DynamicForms/dynamic-form/dynamic-form.component';

import { QuestionService } from '../../../DynamicForms/question.service';
import { QuestionBase } from '../../../DynamicForms/question-base';
import { Observable } from 'rxjs';



@Component({
  selector: 'app-first-aid-record',
  standalone: true,
  imports: [AsyncPipe, DynamicFormComponent],
  providers: [QuestionService],
  templateUrl: './first-aid-record.component.html',
  styleUrl: './first-aid-record.component.css'
})
export class FirstAidRecordComponent {

  questions$: Observable<QuestionBase<any>[]>;
  formTitle = "Unfallbericht"
  private questionService: QuestionService;

  constructor(service: QuestionService) {
    this.questionService = service;
    this.questions$ = service.getQuestions();
  }


  }



