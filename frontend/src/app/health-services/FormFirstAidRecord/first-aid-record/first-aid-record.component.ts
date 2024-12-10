
import { Component,  inject,  OnInit, } from '@angular/core';

import { AsyncPipe } from '@angular/common';

import { DynamicFormComponent } from '../../../DynamicForms/dynamic-form/dynamic-form.component';

import { QuestionService } from '../../../DynamicForms/question.service';
import { QuestionBase } from '../../../DynamicForms/question-base';
import { Observable, of, Subscription} from 'rxjs';

import { MetadataService } from '../../../DynamicForms/services/model.metadata.service';



@Component({
  selector: 'app-first-aid-record',
  standalone: true,
  imports: [AsyncPipe, DynamicFormComponent],
  providers: [QuestionService, MetadataService],
  templateUrl: './first-aid-record.component.html',
  styleUrl: './first-aid-record.component.css'
})
export class FirstAidRecordComponent implements OnInit {

  questions$: Observable<QuestionBase<any>[]> = of([]);
  formTitle = "Unfallbericht"
  private questionservice = inject(QuestionService);
  private dataset = inject(MetadataService);
  private subscription!: Subscription;

  ngOnInit(): void {


      this.subscription = this.dataset.getMetadata("http://127.0.0.1:8000/api/digitalfirstaid/meta/?format=json").subscribe({
        next: (data) => {
            this.questions$ = this.questionservice.getQuestions(data)
        }
      });
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }


  }



