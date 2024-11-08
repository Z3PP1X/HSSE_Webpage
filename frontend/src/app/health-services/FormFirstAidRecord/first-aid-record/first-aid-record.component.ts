import { DUMMY_QUESTIONS_ALT } from './../../../../dummy-questions2';
import { Component } from '@angular/core';
import { SubmittableFormCardComponent } from '../../../components/submittable-form-card/submittable-form-card.component';


@Component({
  selector: 'app-first-aid-record',
  standalone: true,
  imports: [SubmittableFormCardComponent],
  templateUrl: './first-aid-record.component.html',
  styleUrl: './first-aid-record.component.scss'
})
export class FirstAidRecordComponent {

  configurationItem = DUMMY_QUESTIONS_ALT;


}
