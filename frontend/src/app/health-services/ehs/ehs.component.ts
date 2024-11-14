import { Component } from '@angular/core';

import { FirstAidRecordComponent } from '../FormFirstAidRecord/first-aid-record/first-aid-record.component';

@Component({
  selector: 'app-ehs',
  standalone: true,
  imports: [FirstAidRecordComponent],
  templateUrl: './ehs.component.html',
  styleUrl: './ehs.component.scss'
})
export class EhsComponent {

}
