import { Component } from '@angular/core';
import { DUMMY_QUESTIONS } from '../../../dummy-questions';
import { DUMMY_QUESTIONS_ALT } from '../../../dummy-questions2';
import { SubmittableFormCardComponent } from '../../components/submittable-form-card/submittable-form-card.component';

@Component({
  selector: 'app-ehs',
  standalone: true,
  imports: [SubmittableFormCardComponent],
  templateUrl: './ehs.component.html',
  styleUrl: './ehs.component.scss'
})
export class EhsComponent {

  providedData = DUMMY_QUESTIONS

}
