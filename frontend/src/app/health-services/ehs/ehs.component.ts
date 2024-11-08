import { Component } from '@angular/core';
import { SubmittableFormCardComponent } from '../../components/submittable-form-card/submittable-form-card.component';
import { FirstAidRecordComponent } from '../FormFirstAidRecord/first-aid-record/first-aid-record.component';

@Component({
  selector: 'app-ehs',
  standalone: true,
  imports: [SubmittableFormCardComponent, FirstAidRecordComponent],
  templateUrl: './ehs.component.html',
  styleUrl: './ehs.component.scss'
})
export class EhsComponent {

}
