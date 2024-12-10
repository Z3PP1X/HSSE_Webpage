import {Injectable, inject} from '@angular/core';
import { DropdownQuestion } from './questions/question-dropdown';
import {QuestionBase} from './question-base';
import { TextboxQuestion } from './questions/questions-textbox';
import {of} from 'rxjs';
import { LocationQuestion } from './questions/question-location';
import { DateTimeQuestion } from './questions/question-datetime';
import { MetadataService } from './services/model.metadata.service';
import { QuestionMetadata } from './interfaces/question-metadata.interface';
import { TESTQUESTIONS } from './TEST-Questions';

@Injectable({
  providedIn: 'root'
})
export class QuestionService {
  // TODO: get from a remote source of question metadata
  getQuestions(data: any) {
    const imp = TESTQUESTIONS;


    const questions: QuestionBase<string>[] = []

    for (let index = 0; index < imp.length; index++) {

      const element = imp[index];

      switch (element.controlType) {
        case "textbox":
           const textboxquestion = new TextboxQuestion({
            key: element.key,
            label: element.label,
            type: element.type,
            order: element.order
          })
          questions.push(textboxquestion);
          break;
        case "location":
          const locationquestion = new LocationQuestion({
            key: element.key,
            label: element.label,
            type: element.type,
            order: element.order
          })
          questions.push(locationquestion)
          break;
        case "datetime":
          const datetimequestion = new DateTimeQuestion({
            key: element.key,
            label: element.label,
            type: element.type,
            order: element.order
          })
          questions.push(datetimequestion)
          break;
        case "dropdown":
          const dropdownquestion = new DropdownQuestion({
            key: element.key,
            label: element.label,
            type: element.type,
            options: element.options
          })
          questions.push(dropdownquestion)
          break;
      }

    };
    return of(questions.sort((a, b) => a.order - b.order));
  }
}
